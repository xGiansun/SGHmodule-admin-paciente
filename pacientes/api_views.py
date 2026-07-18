"""
Vistas de la API REST para la aplicación de pacientes.

Expone los endpoints necesarios para que un frontend externo
(React, Vue u otro) pueda realizar operaciones CRUD sobre
los pacientes del sistema.

Todos los endpoints requieren autenticación.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Paciente
from .serializers import PacienteSerializer, PacienteListSerializer
from .utils import buscar_pacientes


# Paginación

class PacientePagination(PageNumberPagination):
    """
    Paginación estándar para el listado de pacientes.

    Parámetros GET opcionales:
        page      → número de página (por defecto: 1)
        page_size → resultados por página (por defecto: 10, máximo: 100)
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# Endpoints

class PacienteListCreateView(APIView):
    """
    GET  /api/pacientes/  → Lista paginada de pacientes con búsqueda.
    POST /api/pacientes/  → Crea un nuevo paciente.

    Parámetros GET opcionales:
        buscar    → término de búsqueda (nombre completo o documento)
        page      → número de página
        page_size → resultados por página
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        termino = request.GET.get('buscar', '').strip()
        queryset = Paciente.objects.all().order_by('apellidos', 'nombres')
        sugerencias = None

        if termino:
            queryset, sugerencias = buscar_pacientes(queryset, termino)

        paginador = PacientePagination()
        pagina = paginador.paginate_queryset(queryset, request)
        serializer = PacienteListSerializer(pagina, many=True)

        respuesta = paginador.get_paginated_response(serializer.data)

        # Agrega metadatos de búsqueda a la respuesta
        if termino:
            respuesta.data['busqueda'] = termino
            respuesta.data['hay_resultados'] = queryset.exists()
            if sugerencias is not None:
                respuesta.data['sugerencias'] = PacienteListSerializer(
                    sugerencias, many=True
                ).data

        return respuesta

    def post(self, request):
        serializer = PacienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PacienteDetailView(APIView):
    """
    GET    /api/pacientes/{id}/  → Detalle completo de un paciente.
    PUT    /api/pacientes/{id}/  → Actualiza todos los campos.
    PATCH  /api/pacientes/{id}/  → Actualiza campos específicos.
    DELETE /api/pacientes/{id}/  → Elimina el paciente.
    """
    permission_classes = [IsAuthenticated]

    def _get_paciente(self, pk):
        return get_object_or_404(Paciente, pk=pk)

    def get(self, request, pk):
        paciente = self._get_paciente(pk)
        serializer = PacienteSerializer(paciente)
        return Response(serializer.data)

    def put(self, request, pk):
        paciente = self._get_paciente(pk)
        serializer = PacienteSerializer(paciente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Permite actualizar solo los campos enviados en el body,
        sin necesidad de enviar todos los campos del paciente.
        """
        paciente = self._get_paciente(pk)
        serializer = PacienteSerializer(paciente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        paciente = self._get_paciente(pk)
        paciente.delete()
        return Response(
            {"mensaje": "Paciente eliminado correctamente."},
            status=status.HTTP_200_OK
        )
