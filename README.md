# 🏥 SGH - Sistema de Gestión Hospitalaria

### Módulo de Administración de Pacientes

Proyecto desarrollado como parte del programa **Tecnólogo en Análisis y Desarrollo de Software** - SENA.

---

## 📋 Descripción

Se desarrolló un Módulo de Administración de Pacientes utilizando Django 6 y MySQL. El módulo permite registrar, consultar, editar y eliminar pacientes mediante operaciones CRUD. Además, incorpora autenticación de usuarios con registro desde el navegador, búsqueda de registros, paginación, validación de formularios y un dashboard principal. Para el desarrollo se utilizaron Visual Studio Code, Git, GitHub, Bootstrap 5, Laragon y DBeaver, siguiendo buenas prácticas como el uso de un entorno virtual, variables de entorno, archivo `.gitignore` y `requirements.txt`.

---

## 🛠️ Tecnologías y herramientas utilizadas

### Herramientas de desarrollo

- Visual Studio Code
- Windows PowerShell
- Git / GitHub

### Lenguajes

- Python
- HTML5

### Frameworks y librerías

- Django 6
- Bootstrap 5.3.7
- Bootstrap Icons 1.11.3

### Base de datos

- MySQL

### Herramientas complementarias

- Laragon (servidor MySQL local)
- DBeaver (administración de la base de datos)

### Gestión del proyecto

- Entorno virtual (`.venv`)
- Variables de entorno (`.env`)
- `.gitignore`
- `requirements.txt`

---

## ✅ Funcionalidades

- Registro de cuenta de usuario desde el navegador (`/registro/`)
- Inicio y cierre de sesión
- Dashboard principal con resumen de pacientes
- Registro de pacientes
- Consulta de pacientes
- Actualización de pacientes (con fecha de nacimiento pre-rellena correctamente)
- Eliminación de pacientes con confirmación
- Búsqueda por nombre, apellido y número de documento
- Paginación
- Validación de formularios
- Protección de rutas mediante autenticación
- Gestión de sesiones

---

## ⚙️ Instalación y configuración

> **Requisito previo:** tener **Laragon** corriendo con el servicio MySQL activo antes de ejecutar cualquier comando.

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/xGiansun/SGHmodule-admin-paciente.git
   cd SGHmodule-admin-paciente
   ```

2. Crear y activar el entorno virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crear el archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```env
   SECRET_KEY=tu_clave_secreta
   DEBUG=True
   DB_NAME=nombre_base_datos
   DB_USER=usuario
   DB_PASSWORD=contraseña
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```

5. Aplicar migraciones:
   ```bash
   python manage.py migrate
   ```

6. Iniciar el servidor:
   ```bash
   python manage.py runserver
   ```

---

## 🚀 Primer acceso — Cómo crear tu cuenta

El sistema requiere autenticación para acceder al módulo de pacientes. La cuenta se crea directamente desde el navegador, sin necesidad de comandos adicionales:

1. Con el servidor corriendo, abre tu navegador y ve a:
   ```
   http://127.0.0.1:8000/registro/
   ```

2. Completa el formulario con un nombre de usuario y contraseña.

3. Al registrarte exitosamente, serás redirigido al login automáticamente:
   ```
   http://127.0.0.1:8000/login/
   ```

4. Inicia sesión y accede al sistema.

> ℹ️ Si ya tienes una cuenta creada, ve directamente a `http://127.0.0.1:8000/login/`.

---

## 🐛 Correcciones recientes

| # | Problema | Solución |
|---|----------|----------|
| 1 | El sistema requería login pero no había forma de crear un usuario desde el navegador | Se agregó la vista `/registro/` con formulario `UserCreationForm` de Django |
| 2 | Al editar un paciente, el campo **Fecha de nacimiento** aparecía vacío y debía ingresarse de nuevo | Se declaró `fecha_nacimiento` explícitamente en el formulario con `input_formats` y `format='%Y-%m-%d'` para garantizar que el valor se pre-rellene correctamente |

---

## 👤👤 Autores
  
GitHub: [@xGiansun](https://github.com/xGiansun)
GitHub: [Wilson Corredor](https://github.com/wilsoncorredor1123)
