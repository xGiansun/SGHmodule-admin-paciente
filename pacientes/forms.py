"""
Módulo de formularios para la aplicación de pacientes.

Define los formularios de entrada de datos utilizados en la creación
y edición de pacientes dentro del sistema hospitalario.
"""

from django import forms
from django.utils import timezone
from datetime import date
from .models import Paciente


class PacienteForm(forms.ModelForm):
    """
    Formulario para registrar o editar la información de un paciente.

    Basado en el modelo Paciente. Incluye estilos Bootstrap, etiquetas
    en español, mensajes de error personalizados y validaciones de negocio.
    """

    class Meta:
        model = Paciente
        fields = [
            'tipo_documento',
            'numero_documento',
            'nombres',
            'apellidos',
            'fecha_nacimiento',
            'telefono',
            'correo',
            'direccion',
        ]

        labels = {
            'tipo_documento': 'Tipo de documento',
            'numero_documento': 'Número de documento',
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'telefono': 'Teléfono',
            'correo': 'Correo electrónico',
            'direccion': 'Dirección',
        }

        widgets = {
            'tipo_documento': forms.Select(attrs={
                'class': 'form-select',
            }),
            'numero_documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de documento',
                'maxlength': '20',
            }),
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese los nombres',
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese los apellidos',
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el teléfono',
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com',
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección',
            }),
        }

        error_messages = {
            'numero_documento': {
                'unique': 'Ya existe un paciente registrado con ese número de documento.',
            }
        }

    def clean_fecha_nacimiento(self):
        """
        Valida que la fecha de nacimiento sea coherente:
        - No puede ser una fecha futura.
        - No puede corresponder a una persona de más de 130 años.
        """
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if fecha:
            hoy = timezone.now().date()
            if fecha > hoy:
                raise forms.ValidationError(
                    'La fecha de nacimiento no puede ser una fecha futura.'
                )
            edad = (hoy - fecha).days // 365
            if edad > 130:
                raise forms.ValidationError(
                    'La fecha de nacimiento ingresada no es válida. La edad no puede superar los 130 años.'
                )
        return fecha

    def clean_telefono(self):
        """
        Valida que el teléfono contenga únicamente dígitos, espacios,
        guiones o el signo +. No se permiten letras ni otros caracteres.
        """
        telefono = self.cleaned_data.get('telefono', '').strip()
        caracteres_validos = set('0123456789 +-')
        if not all(c in caracteres_validos for c in telefono):
            raise forms.ValidationError(
                'El teléfono solo puede contener números, espacios, guiones o el signo +.'
            )
        return telefono
