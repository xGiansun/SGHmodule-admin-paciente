"""
Rutas de la API REST para el módulo de pacientes.

Se montan bajo el prefijo /api/ definido en hospital/urls.py.

Endpoints disponibles:
    GET    /api/pacientes/        → Listado con búsqueda y paginación
    POST   /api/pacientes/        → Crear paciente
    GET    /api/pacientes/{id}/   → Detalle de un paciente
    PUT    /api/pacientes/{id}/   → Actualizar paciente (todos los campos)
    PATCH  /api/pacientes/{id}/   → Actualizar paciente (campos parciales)
    DELETE /api/pacientes/{id}/   → Eliminar paciente
"""

from django.urls import path
from .api_views import PacienteListCreateView, PacienteDetailView

urlpatterns = [
    path('pacientes/', PacienteListCreateView.as_view(), name='api_pacientes'),
    path('pacientes/<int:pk>/', PacienteDetailView.as_view(), name='api_paciente_detail'),
]
