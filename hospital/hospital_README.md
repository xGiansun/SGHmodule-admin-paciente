# Módulo `hospital`

Módulo de configuración del proyecto Django SGH (Sistema de Gestión Hospitalaria). Contiene los ajustes globales del proyecto, el enrutador principal de URLs y las vistas de autenticación de la API REST.

---

## Archivos del módulo

```
hospital/
├── settings.py    # Configuración global del proyecto Django
├── urls.py        # Enrutador principal de URLs
├── auth_views.py  # Vistas de autenticación para la API REST
├── asgi.py        # Punto de entrada ASGI (despliegue asíncrono)
└── wsgi.py        # Punto de entrada WSGI (despliegue tradicional)
```

---

## Configuración — `settings.py`

Las variables sensibles se cargan desde el archivo `.env` mediante `python-decouple`. No se almacenan valores reales en el código fuente.

| Variable de entorno | Uso en settings                            |
|---------------------|--------------------------------------------|
| `SECRET_KEY`        | Clave criptográfica de Django              |
| `DEBUG`             | Modo de depuración (True/False)            |
| `DB_NAME`           | Nombre de la base de datos MySQL           |
| `DB_USER`           | Usuario de MySQL                           |
| `DB_PASSWORD`       | Contraseña de MySQL                        |
| `DB_HOST`           | Host de MySQL (por defecto: 127.0.0.1)     |
| `DB_PORT`           | Puerto de MySQL (por defecto: 3306)        |

Aplicaciones instaladas relevantes:
- `pacientes` — módulo principal del sistema
- `rest_framework` — Django REST Framework
- `corsheaders` — manejo de CORS para el frontend externo

---

## Enrutador principal — `urls.py`

| Prefijo URL           | Destino                          | Descripción                        |
|-----------------------|----------------------------------|------------------------------------|
| `/admin/`             | `admin.site`                     | Panel de administración de Django  |
| `/login/`             | `auth_views.LoginView`           | Login HTML                         |
| `/logout/`            | `auth_views.LogoutView`          | Logout HTML                        |
| `/registro/`          | `pacientes.views.registro_usuario` | Registro de nuevo usuario        |
| `/`                   | `pacientes.urls`                 | Todas las rutas del módulo pacientes |
| `/api/auth/login/`    | `LoginAPIView`                   | Login por API REST (devuelve token)|
| `/api/auth/logout/`   | `LogoutAPIView`                  | Logout por API REST                |
| `/api/auth/me/`       | `MeAPIView`                      | Datos del usuario autenticado      |
| `/api/`               | `pacientes.api_urls`             | Endpoints CRUD de pacientes        |

---

## Autenticación de la API REST — `auth_views.py`

El sistema implementa autenticación por **token** (Django REST Framework `TokenAuthentication`).

### Endpoints

#### `POST /api/auth/login/`

Autentica un usuario y devuelve un token de acceso.

**Cuerpo de la petición:**
```json
{
  "username": "admin",
  "password": "mi_contraseña"
}
```

**Respuesta exitosa (200):**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "username": "admin"
}
```

**Uso del token en peticiones posteriores:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

#### `POST /api/auth/logout/`

Invalida el token del servidor. El frontend debe eliminar el token almacenado localmente.

**Respuesta exitosa (200):**
```json
{
  "mensaje": "Sesión cerrada correctamente."
}
```

---

#### `GET /api/auth/me/`

Devuelve información básica del usuario autenticado.

**Respuesta exitosa (200):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@hospital.com"
}
```
