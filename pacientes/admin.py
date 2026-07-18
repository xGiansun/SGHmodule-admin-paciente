"""
Configuración del panel de administración para la aplicación de pacientes.

Registra el modelo Paciente con opciones avanzadas de visualización,
búsqueda y filtrado en el admin de Django.
"""

from django.contrib import admin
from .models import Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Paciente en el panel de administración.

    Permite visualizar, buscar y filtrar pacientes de forma eficiente.
    El campo 'fecha_registro' es de solo lectura al ser generado automáticamente.
    """

    list_display = (
        'tipo_documento',
        'numero_documento',
        'nombres',
        'apellidos',
        'telefono',
        'correo',
        'fecha_registro',
    )

    search_fields = (
        'numero_documento',
        'nombres',
        'apellidos',
    )

    list_filter = (
        'tipo_documento',
        'fecha_registro',
    )

    readonly_fields = (
        'fecha_registro',
    )

    ordering = (
        'apellidos',
        'nombres',
    )
