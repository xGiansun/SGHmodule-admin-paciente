"""
Módulo de modelos para la aplicación de pacientes.

Define la estructura de datos que representa a un paciente
dentro del sistema hospitalario.
"""

from django.db import models


class Paciente(models.Model):
    """
    Modelo que representa a un paciente registrado en el sistema hospitalario.

    Almacena la información personal, de contacto y de identificación
    de cada paciente. El número de documento es único por paciente.
    """

    TIPOS_DOCUMENTO = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
        ('PP', 'Pasaporte'),
    ]

    tipo_documento = models.CharField(
        max_length=2,
        choices=TIPOS_DOCUMENTO,
        default='CC',
        verbose_name='Tipo de documento'
    )

    numero_documento = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de documento'
    )

    nombres = models.CharField(
        max_length=100,
        verbose_name='Nombres'
    )

    apellidos = models.CharField(
        max_length=100,
        verbose_name='Apellidos'
    )

    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de nacimiento'
    )

    telefono = models.CharField(
        max_length=20,
        verbose_name='Teléfono'
    )

    correo = models.EmailField(
        verbose_name='Correo electrónico'
    )

    direccion = models.CharField(
        max_length=200,
        verbose_name='Dirección'
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de registro'
    )

    class Meta:
        ordering = ['apellidos', 'nombres']
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        """Retorna una representación legible del paciente."""
        return f"{self.tipo_documento} {self.numero_documento} - {self.nombres} {self.apellidos}"
