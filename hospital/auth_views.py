"""
Vistas de autenticación para la API REST.

Endpoints:
    POST /api/auth/login/   → recibe usuario y contraseña, devuelve token
    POST /api/auth/logout/  → invalida el token actual
    GET  /api/auth/me/      → devuelve datos del usuario autenticado
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class LoginAPIView(APIView):
    """
    POST /api/auth/login/
    Body : { "username": "...", "password": "..." }
    Respuesta exitosa: { "token": "abc123...", "username": "..." }

    El token obtenido debe enviarse en todas las peticiones posteriores
    como encabezado HTTP:
        Authorization: Token abc123...
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()

        if not username or not password:
            return Response(
                {'error': 'Se requieren usuario y contraseña.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response(
                {'error': 'Credenciales incorrectas.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'username': user.username,
        })


class LogoutAPIView(APIView):
    """
    POST /api/auth/logout/
    Header: Authorization: Token abc123...

    Elimina el token del servidor, invalidando la sesión.
    El frontend debe borrar el token almacenado localmente.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({'mensaje': 'Sesión cerrada correctamente.'})


class MeAPIView(APIView):
    """
    GET /api/auth/me/
    Header: Authorization: Token abc123...

    Devuelve información básica del usuario autenticado.
    Útil para que el frontend sepa quién está logueado sin
    tener que almacenar esa información por separado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
        })
