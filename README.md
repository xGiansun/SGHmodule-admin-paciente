# SGH - Sistema de Gestion Hospitalaria
### Modulo de Administracion de Pacientes

Proyecto desarrollado como parte del programa Tecnologo en Analisis y Desarrollo de Software - SENA.

---

## Descripcion

Sistema de gestion hospitalaria con modulo completo de administracion de pacientes. Incluye interfaz web con templates Django y una API REST para integracion con frontends externos (React, Vue, etc.).

---

## Stack tecnologico

| Categoria | Tecnologia |
|---|---|
| Lenguaje | Python |
| Framework backend | Django 6 |
| API REST | Django REST Framework |
| Base de datos | MySQL |
| Frontend web | HTML5 + Bootstrap 5.3.7 |
| Versionamiento | Git + GitHub |
| Entorno local | Laragon + DBeaver |
| IDE | Visual Studio Code |

---

## Funcionalidades

### Interfaz web
- Login y logout con sesiones
- Dashboard con resumen de pacientes
- CRUD completo de pacientes
- Busqueda por nombre completo o documento
- Sugerencias cuando no hay resultados exactos
- Paginacion y validacion de formularios
- Advertencia al registrar correos compartidos temporalmente
- Validacion de fecha de nacimiento y telefono

### API REST

| Metodo | Endpoint | Descripcion |
|---|---|---|
| POST | `/api/auth/login/` | Obtener token de acceso |
| POST | `/api/auth/logout/` | Cerrar sesion e invalidar token |
| GET | `/api/auth/me/` | Datos del usuario autenticado |
| GET | `/api/pacientes/` | Listar pacientes con busqueda y paginacion |
| POST | `/api/pacientes/` | Crear paciente |
| GET | `/api/pacientes/{id}/` | Detalle de un paciente |
| PUT | `/api/pacientes/{id}/` | Actualizar paciente completo |
| PATCH | `/api/pacientes/{id}/` | Actualizar campos especificos |
| DELETE | `/api/pacientes/{id}/` | Eliminar paciente |

---

## Instalacion

> Requiere Laragon corriendo con MySQL activo antes de ejecutar.

```bash
# 1. Clonar el repositorio
git clone https://github.com/xGiansun/SGHmodule-admin-paciente.git
cd SGHmodule-admin-paciente

# 2. Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# 3. Instalar dependencias
python -m pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env
# Abre el archivo .env y completa tus credenciales de MySQL y SECRET_KEY

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear usuario administrador (obligatorio para acceder al sistema)
python manage.py createsuperuser

# 7. Iniciar servidor
python manage.py runserver
```

El sistema estara disponible en http://127.0.0.1:8000 (entorno local de desarrollo)

---

## Uso de la API

```
# 1. Obtener token
POST /api/auth/login/
Body: { "username": "admin", "password": "tu_password" }
Respuesta: { "token": "abc123...", "username": "admin" }

# 2. Incluir el token en cada peticion como header
Authorization: Token abc123...
```

---

## Estructura del proyecto

```
SGHmodule-admin-paciente/
├── hospital/
│   ├── __init__.py
│   ├── asgi.py
│   ├── auth_views.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pacientes/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_paciente_numero_documento.py
│   │   ├── 0003_alter_paciente_tipo_documento.py
│   │   └── __init__.py
│   ├── templates/
│   │   └── pacientes/
│   │       ├── confirmar_eliminar.html
│   │       ├── dashboard.html
│   │       ├── formulario.html
│   │       └── lista.html
│   ├── admin.py
│   ├── api_urls.py
│   ├── api_views.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── static/
│   └── css/
├── templates/
│   ├── base.html
│   └── registration/
│       └── login.html
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## Autor

**Giansun**
GitHub: [@xGiansun](https://github.com/xGiansun)
