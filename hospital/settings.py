"""
Configuración del proyecto SistemaHospitalario (Django).

Contiene los parámetros de configuración para el entorno de desarrollo.
SECRET_KEY y credenciales de base de datos
a variables de entorno usando python-decouple o django-environ.

Referencia: https://docs.djangoproject.com/en/6.0/topics/settings/
"""

import os
from pathlib import Path
from decouple import config

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================
# Seguridad
# ==========================
SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# ==========================
# Aplicaciones instaladas
# ==========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # API REST
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    # Aplicaciones del proyecto
    'pacientes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',          # CORS — debe ir antes de CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hospital.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hospital.wsgi.application'


# ==========================
# Base de datos
# ==========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}


# ==========================
# Validación de contraseñas
# ==========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==========================
# Internacionalización
# ==========================
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True


# ==========================
# Archivos estáticos
# ==========================
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


# ==========================
# Tipo de clave primaria por defecto
# ==========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================
# Configuración de autenticación
# ==========================
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'


# ==========================
# Configuración de sesiones
# ==========================
SESSION_COOKIE_AGE = 1800
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# ==========================
# Django REST Framework
# ==========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # Token: para el frontend separado (React/Vue)
        'rest_framework.authentication.TokenAuthentication',
        # Session: mantiene compatibilidad con el login HTML actual
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}


# ==========================
# CORS (Cross-Origin Resource Sharing)
# Permite que el frontend (React/Vue en otro puerto) acceda a la API.
# En producción reemplaza CORS_ALLOW_ALL_ORIGINS por CORS_ALLOWED_ORIGINS.
# ==========================
CORS_ALLOW_ALL_ORIGINS = True          # Solo para desarrollo local
# CORS_ALLOWED_ORIGINS = [            # Usar esto en producción:
#     "http://localhost:3000",         #   Puerto de React
#     "http://localhost:5173",         #   Puerto de Vite (Vue)
# ]