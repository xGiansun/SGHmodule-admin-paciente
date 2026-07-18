"""
Utilidades compartidas de la aplicación de pacientes.

Centraliza lógica reutilizable para evitar duplicación entre las vistas
de templates HTML (views.py) y las vistas de la API REST (api_views.py).
"""

from django.db.models import Q
from .models import Paciente


def buscar_pacientes(queryset, termino):
    """
    Aplica un filtro de búsqueda inteligente sobre un queryset de Paciente.

    Estrategia:
      1. Divide el término en palabras individuales.
      2. Exige que CADA palabra aparezca en 'nombres' O en 'apellidos'
         (AND entre palabras, OR entre campos), lo que permite encontrar
         a un paciente buscando "Juan Pérez", "Pérez Juan" o solo "Juan".
      3. También acepta coincidencia parcial con el número de documento.
      4. Si no hay resultados exactos, calcula sugerencias: pacientes que
         compartan AL MENOS UNA palabra con la búsqueda (útil cuando el
         nombre fue escrito de forma incompleta o con algún error).
         Las palabras de 1-2 caracteres se ignoran en sugerencias para
         evitar resultados demasiado amplios.

    Args:
        queryset: QuerySet de Paciente sobre el que aplicar el filtro.
        termino (str): Término de búsqueda ingresado por el usuario.

    Returns:
        tuple(QuerySet, QuerySet | None):
            - Primer elemento: resultados exactos (puede ser vacío).
            - Segundo elemento: sugerencias si no hay resultados exactos,
              None si sí los hay.
    """
    palabras = termino.split()

    filtro_documento = Q(numero_documento__icontains=termino)

    filtro_nombre = Q()
    for palabra in palabras:
        filtro_nombre &= (
            Q(nombres__icontains=palabra) | Q(apellidos__icontains=palabra)
        )

    resultados = queryset.filter(filtro_documento | filtro_nombre)

    if resultados.exists():
        return resultados, None

    # Sin resultados exactos → calcular sugerencias
    filtro_sugerencias = Q()
    hay_palabras_utiles = False
    for palabra in palabras:
        if len(palabra) >= 3:
            hay_palabras_utiles = True
            filtro_sugerencias |= (
                Q(nombres__icontains=palabra) | Q(apellidos__icontains=palabra)
            )

    sugerencias = None
    if hay_palabras_utiles:
        sugerencias = (
            Paciente.objects
            .filter(filtro_sugerencias)
            .order_by('apellidos', 'nombres')[:5]
        )

    return Paciente.objects.none(), sugerencias
