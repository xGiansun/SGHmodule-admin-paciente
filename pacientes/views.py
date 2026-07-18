"""
Módulo de vistas para la aplicación de pacientes.

Contiene las vistas que gestionan el ciclo de vida de un paciente:
dashboard, listado, creación, edición y eliminación.
Todas las vistas requieren autenticación del usuario.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Paciente
from .forms import PacienteForm
from .utils import buscar_pacientes


@login_required
def dashboard(request):
    """
    Vista principal del sistema. Muestra un resumen del estado actual:
    total de pacientes registrados y los últimos 5 ingresados al sistema.
    """
    total_pacientes = Paciente.objects.count()
    ultimos_pacientes = Paciente.objects.order_by('-fecha_registro')[:5]

    contexto = {
        'total_pacientes': total_pacientes,
        'ultimos_pacientes': ultimos_pacientes,
    }

    return render(request, 'pacientes/dashboard.html', contexto)


@login_required
def lista_pacientes(request):
    """
    Muestra el listado paginado de todos los pacientes registrados.

    Permite buscar por nombre completo (en cualquier orden), nombre o
    apellido parcial, o número de documento. La búsqueda por nombre exige
    que TODAS las palabras ingresadas coincidan con el nombre o el
    apellido del paciente (sin importar en cuál de los dos campos caiga
    cada una), lo que permite encontrar tanto "Juan Pérez" como
    "Pérez Juan" o simplemente "Juan".

    Si la búsqueda no arroja resultados exactos, se calcula una lista de
    posibles coincidencias (pacientes que comparten al menos una palabra
    con lo buscado), útil cuando el nombre se digitó de forma incompleta
    o con algún error.

    Parámetros GET:
        buscar (str): Término de búsqueda opcional.
        page (int): Número de página para la paginación.
    """
    termino_busqueda = request.GET.get('buscar', '').strip()
    pacientes = Paciente.objects.all().order_by('apellidos', 'nombres')
    sugerencias = None

    if termino_busqueda:
        pacientes, sugerencias = buscar_pacientes(pacientes, termino_busqueda)

    paginador = Paginator(pacientes, 5)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginador.get_page(numero_pagina)

    return render(request, 'pacientes/lista.html', {
        'page_obj': pagina_actual,
        'busqueda': termino_busqueda,
        'sugerencias': sugerencias,
    })


@login_required
def crear_paciente(request):
    """
    Permite registrar un nuevo paciente en el sistema.

    GET: Muestra el formulario vacío de registro.
    POST: Valida y guarda el nuevo paciente. Si el correo ingresado ya
    pertenece a otro paciente, muestra una advertencia con el nombre de
    ese paciente y solicita confirmación antes de continuar.
    """
    if request.method == 'POST':
        formulario = PacienteForm(request.POST)
        correo = request.POST.get('correo', '').strip()
        confirmar = request.POST.get('confirmar_correo_duplicado')

        paciente_con_correo = Paciente.objects.filter(correo=correo).first()

        if paciente_con_correo and not confirmar:
            return render(request, 'pacientes/formulario.html', {
                'formulario': formulario,
                'advertencia_correo': paciente_con_correo,
            })

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Paciente registrado correctamente.')
            return redirect('lista_pacientes')
    else:
        formulario = PacienteForm()

    return render(request, 'pacientes/formulario.html', {
        'formulario': formulario,
    })


@login_required
def editar_paciente(request, paciente_id):
    """
    Permite actualizar la información de un paciente existente.

    Args:
        paciente_id (int): Identificador único del paciente a editar.

    GET: Muestra el formulario con los datos actuales del paciente.
    POST: Valida y guarda los cambios. Si el correo pertenece a otro
    paciente distinto al que se está editando, muestra advertencia y
    solicita confirmación.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        formulario = PacienteForm(request.POST, instance=paciente)
        correo = request.POST.get('correo', '').strip()
        confirmar = request.POST.get('confirmar_correo_duplicado')

        paciente_con_correo = Paciente.objects.filter(correo=correo).exclude(id=paciente_id).first()

        if paciente_con_correo and not confirmar:
            return render(request, 'pacientes/formulario.html', {
                'formulario': formulario,
                'advertencia_correo': paciente_con_correo,
            })

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Paciente actualizado correctamente.')
            return redirect('lista_pacientes')
    else:
        formulario = PacienteForm(instance=paciente)

    return render(request, 'pacientes/formulario.html', {
        'formulario': formulario,
    })


@login_required
def eliminar_paciente(request, paciente_id):
    """
    Permite eliminar un paciente del sistema tras una confirmación explícita.

    Args:
        paciente_id (int): Identificador único del paciente a eliminar.

    GET: Muestra la pantalla de confirmación de eliminación.
    POST: Ejecuta la eliminación y redirige al listado.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        paciente.delete()
        messages.success(request, 'Paciente eliminado correctamente.')
        return redirect('lista_pacientes')

    return render(request, 'pacientes/confirmar_eliminar.html', {
        'paciente': paciente,
    })
