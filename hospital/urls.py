"""
Configuración de rutas URL del proyecto SistemaHospitalario.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .auth_views import LoginAPIView, LogoutAPIView, MeAPIView
from pacientes.views import registro_usuario


urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticación HTML
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', registro_usuario, name='registro'),

    # Módulo de pacientes
    path('', include('pacientes.urls')),

    # API REST
    path('api/auth/login/',  LoginAPIView.as_view(),  name='api_login'),
    path('api/auth/logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('api/auth/me/',     MeAPIView.as_view(),     name='api_me'),
    path('api/', include('pacientes.api_urls')),
]
