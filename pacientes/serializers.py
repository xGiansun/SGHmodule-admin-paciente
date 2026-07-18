"""
Serializadores para la aplicación de pacientes.

Convierten instancias del modelo Paciente a JSON (y viceversa)
para ser usadas en los endpoints de la API REST.
"""

from rest_framework import serializers
from .models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    """
    Serializador completo del modelo Paciente.

    Campos de solo lectura:
        - id, fecha_registro: generados automáticamente por el sistema.
        - tipo_documento_display: versión legible del tipo de documento
          (ej. "Cédula de Ciudadanía" en vez de "CC").
        - nombre_completo: nombres + apellidos concatenados, útil para
          el frontend sin que tenga que construirlo manualmente.
    """

    tipo_documento_display = serializers.CharField(
        source='get_tipo_documento_display',
        read_only=True,
    )
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Paciente
        fields = [
            'id',
            'tipo_documento',
            'tipo_documento_display',
            'numero_documento',
            'nombres',
            'apellidos',
            'nombre_completo',
            'fecha_nacimiento',
            'telefono',
            'correo',
            'direccion',
            'fecha_registro',
        ]
        read_only_fields = ['id', 'fecha_registro', 'tipo_documento_display', 'nombre_completo']

    def get_nombre_completo(self, obj):
        """Devuelve el nombre completo del paciente: 'nombres apellidos'."""
        return f"{obj.nombres} {obj.apellidos}"

    def validate_numero_documento(self, value):
        """
        Valida que el número de documento sea único.
        En edición excluye el propio registro para no generar falsos positivos.
        """
        qs = Paciente.objects.filter(numero_documento=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "Ya existe un paciente registrado con este número de documento."
            )
        return value


class PacienteListSerializer(serializers.ModelSerializer):
    """
    Serializador ligero para el listado de pacientes.
    Devuelve solo los campos necesarios para mostrar en tabla,
    reduciendo el tamaño de la respuesta cuando hay muchos registros.
    """

    tipo_documento_display = serializers.CharField(
        source='get_tipo_documento_display',
        read_only=True,
    )
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Paciente
        fields = [
            'id',
            'tipo_documento_display',
            'numero_documento',
            'nombre_completo',
            'telefono',
            'correo',
        ]

    def get_nombre_completo(self, obj):
        return f"{obj.nombres} {obj.apellidos}"
