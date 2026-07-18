"""
Definición de rutas URL para la aplicación de pacientes.

Mapea cada URL a su vista correspondiente dentro del módulo de pacientes.
"""

from django.urls import path
from . import views


urlpatterns = [
    # Panel principal
    path('', views.dashboard, name='dashboard'),

    # Listado de pacientes (con búsqueda y paginación)
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),

    # Registro de nuevo paciente
    path('pacientes/nuevo/', views.crear_paciente, name='crear_paciente'),

    # Edición de paciente existente
    path(
        'pacientes/editar/<int:paciente_id>/',
        views.editar_paciente,
        name='editar_paciente'
    ),

    # Eliminación de paciente con confirmación
    path(
        'pacientes/eliminar/<int:paciente_id>/',
        views.eliminar_paciente,
        name='eliminar_paciente'
    ),
]
