# Módulo `pacientes`

Aplicación Django que gestiona el ciclo de vida completo de un paciente dentro del Sistema de Gestión Hospitalaria (SGH). Expone dos interfaces: una web con plantillas HTML y Bootstrap, y una API REST con Django REST Framework.

---

## Modelo de datos

### `Paciente`

| Campo              | Tipo                    | Restricciones                          | Descripción                         |
|--------------------|-------------------------|----------------------------------------|-------------------------------------|
| `id`               | `BigAutoField`          | PK, auto                               | Identificador único                 |
| `tipo_documento`   | `CharField(2)`          | choices: CC, TI, CE, PP · default: CC | Tipo de documento de identidad      |
| `numero_documento` | `CharField(20)`         | único                                  | Número de documento del paciente    |
| `nombres`          | `CharField(100)`        | —                                      | Nombres del paciente                |
| `apellidos`        | `CharField(100)`        | —                                      | Apellidos del paciente              |
| `fecha_nacimiento` | `DateField`             | —                                      | Fecha de nacimiento                 |
| `telefono`         | `CharField(20)`         | solo dígitos, espacios, +, -           | Teléfono de contacto                |
| `correo`           | `EmailField(254)`       | —                                      | Correo electrónico                  |
| `direccion`        | `CharField(200)`        | —                                      | Dirección de residencia             |
| `fecha_registro`   | `DateTimeField`         | auto_now_add                           | Fecha y hora de creación del registro |

Ordenamiento por defecto: `apellidos`, `nombres`.

---

## Archivos del módulo

```
pacientes/
├── models.py        # Modelo Paciente
├── views.py         # Vistas HTML (CRUD + dashboard)
├── api_views.py     # Vistas de la API REST
├── api_urls.py      # Rutas de la API
├── urls.py          # Rutas HTML
├── forms.py         # Formulario PacienteForm con validaciones
├── serializers.py   # PacienteSerializer y PacienteListSerializer
├── utils.py         # Búsqueda inteligente buscar_pacientes()
├── admin.py         # Registro en el panel de administración de Django
├── apps.py          # Configuración de la aplicación
├── tests.py         # Casos de prueba
└── migrations/      # Migraciones de base de datos (0001 → 0006)
    templates/
    └── pacientes/
        ├── dashboard.html          # Panel principal
        ├── lista.html              # Listado con búsqueda y paginación
        ├── formulario.html         # Creación y edición de paciente
        └── confirmar_eliminar.html # Confirmación de eliminación
```

---

## Rutas HTML

| URL                                  | Nombre            | Vista               | Descripción                        |
|--------------------------------------|-------------------|---------------------|------------------------------------|
| `/`                                  | `dashboard`       | `dashboard`         | Panel principal con resumen        |
| `/pacientes/`                        | `lista_pacientes` | `lista_pacientes`   | Listado paginado con búsqueda      |
| `/pacientes/nuevo/`                  | `crear_paciente`  | `crear_paciente`    | Formulario de registro             |
| `/pacientes/editar/<id>/`            | `editar_paciente` | `editar_paciente`   | Formulario de edición              |
| `/pacientes/eliminar/<id>/`          | `eliminar_paciente` | `eliminar_paciente` | Confirmación y eliminación       |

Todas las rutas requieren autenticación (`@login_required`).

---

## Rutas de la API REST

Prefijo base: `/api/`  
Autenticación requerida: `Authorization: Token <token>`

| Método   | URL                        | Descripción                              |
|----------|----------------------------|------------------------------------------|
| `GET`    | `/api/pacientes/`          | Listado paginado (soporta `?buscar=`)    |
| `POST`   | `/api/pacientes/`          | Crear nuevo paciente                     |
| `GET`    | `/api/pacientes/<id>/`     | Detalle completo de un paciente          |
| `PUT`    | `/api/pacientes/<id>/`     | Actualizar todos los campos              |
| `PATCH`  | `/api/pacientes/<id>/`     | Actualizar campos específicos            |
| `DELETE` | `/api/pacientes/<id>/`     | Eliminar paciente                        |

### Parámetros GET opcionales (listado)

| Parámetro   | Descripción                                      |
|-------------|--------------------------------------------------|
| `buscar`    | Búsqueda por nombre completo o número de documento |
| `page`      | Número de página (default: 1)                    |
| `page_size` | Resultados por página (default: 10, máx: 100)    |

### Ejemplo de cuerpo POST / PUT

```json
{
  "tipo_documento": "CC",
  "numero_documento": "1234567890",
  "nombres": "María",
  "apellidos": "Gómez Torres",
  "fecha_nacimiento": "1990-05-14",
  "telefono": "3001234567",
  "correo": "maria.gomez@example.com",
  "direccion": "Calle 10 # 5-20, Armenia"
}
```

### Ejemplo de respuesta GET detalle

```json
{
  "id": 1,
  "tipo_documento": "CC",
  "tipo_documento_display": "Cédula de Ciudadanía",
  "numero_documento": "1234567890",
  "nombres": "María",
  "apellidos": "Gómez Torres",
  "nombre_completo": "María Gómez Torres",
  "fecha_nacimiento": "1990-05-14",
  "telefono": "3001234567",
  "correo": "maria.gomez@example.com",
  "direccion": "Calle 10 # 5-20, Armenia",
  "fecha_registro": "2026-08-10T14:32:00Z"
}
```

---

## Validaciones del formulario

| Campo              | Validación                                                                 |
|--------------------|----------------------------------------------------------------------------|
| `numero_documento` | Único en el sistema. Error personalizado si ya existe.                     |
| `fecha_nacimiento` | No puede ser futura. Edad máxima: 130 años.                                |
| `telefono`         | Solo dígitos, espacios, guiones (`-`) y signo (`+`).                       |
| `correo`           | Si ya pertenece a otro paciente, se muestra advertencia y pide confirmación. |

---

## Utilidad de búsqueda — `buscar_pacientes()`

Ubicada en `utils.py`. Estrategia de búsqueda:

1. Divide el término en palabras individuales.
2. Exige que **cada palabra** aparezca en `nombres` **o** en `apellidos` (AND entre palabras, OR entre campos), permitiendo buscar "Juan Pérez", "Pérez Juan" o solo "Pérez".
3. También acepta coincidencia parcial con el número de documento.
4. Si no hay resultados exactos, calcula **sugerencias**: pacientes que compartan al menos una palabra (≥ 3 caracteres) con el término buscado.

---

## Migraciones

| Migración | Descripción                                              |
|-----------|----------------------------------------------------------|
| `0001`    | Creación inicial del modelo `Paciente`                   |
| `0002`    | `numero_documento` → `unique=True`                       |
| `0003`    | `tipo_documento` → choices (CC, TI, CE, PP)              |
| `0004`    | Ajuste de opciones, ordering y `verbose_name`            |
| `0005`    | Ajuste del campo `correo` (EmailField)                   |
| `0006`    | Ajuste adicional del campo `correo`                      |
