"""
Configuración de rutas URL del proyecto SistemaHospitalario.

Incluye las rutas de autenticación (login/logout) y delega
las rutas del sistema al módulo de pacientes.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .auth_views import LoginAPIView, LogoutAPIView, MeAPIView


urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # Autenticación HTML (para los templates actuales)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Módulo de pacientes (templates HTML)
    path('', include('pacientes.urls')),

    # API REST — autenticación (devuelve/invalida token JSON)
    path('api/auth/login/',  LoginAPIView.as_view(),  name='api_login'),
    path('api/auth/logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('api/auth/me/',     MeAPIView.as_view(),     name='api_me'),

    # API REST — CRUD de pacientes
    path('api/', include('pacientes.api_urls')),
]
