"""
Configuración de la aplicación 'pacientes'.

Define los metadatos y ajustes base de la app dentro del proyecto Django.
"""

from django.apps import AppConfig


class PacientesConfig(AppConfig):
    """Configuración principal de la aplicación de gestión de pacientes."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pacientes'
    verbose_name = 'Gestión de Pacientes'
