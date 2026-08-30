"""
Módulo de pruebas automatizadas del Sistema de Gestión Hospitalaria (SGH).

Cubre los casos de prueba TC-01 a TC-10 del Acta de Pruebas y Aceptación.
Cada clase agrupa pruebas por funcionalidad y documenta explícitamente
el resultado esperado versus el resultado obtenido.

Ejecutar con:
    python manage.py test pacientes --settings=hospital.test_settings -v 2
"""

import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import Paciente


# ===========================================================================
# Datos de prueba reutilizables
# ===========================================================================

PACIENTE_VALIDO = {
    'tipo_documento': 'CC',
    'numero_documento': '1234567890',
    'nombres': 'Juan',
    'apellidos': 'Perez Garcia',
    'fecha_nacimiento': '1990-05-15',
    'telefono': '3001234567',
    'correo': 'juan.perez@email.com',
    'direccion': 'Calle 10 # 20-30, Bogota',
}

PACIENTE_2 = {
    'tipo_documento': 'TI',
    'numero_documento': '9876543210',
    'nombres': 'Maria',
    'apellidos': 'Lopez Hernandez',
    'fecha_nacimiento': '2000-08-20',
    'telefono': '3109876543',
    'correo': 'maria.lopez@email.com',
    'direccion': 'Av. 30 # 45-60, Cali',
}

PACIENTE_3 = {
    'tipo_documento': 'CE',
    'numero_documento': '5555555555',
    'nombres': 'Carlos',
    'apellidos': 'Rodriguez Torres',
    'fecha_nacimiento': '1985-03-10',
    'telefono': '3205555555',
    'correo': 'carlos.rodriguez@email.com',
    'direccion': 'Carrera 5 # 12-34, Medellin',
}


# ===========================================================================
# TC-01: Autenticacion HTML
# ===========================================================================

class TC01_AutenticacionLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(
            username='admin_sgh', password='SGH2026@seguro'
        )
        self.url_login = reverse('login')

    def test_01a_login_credenciales_validas(self):
        respuesta = self.client.post(self.url_login, {
            'username': 'admin_sgh',
            'password': 'SGH2026@seguro',
        })
        self.assertEqual(respuesta.status_code, 302)
        self.assertRedirects(respuesta, '/', fetch_redirect_response=False)

    def test_01b_login_password_incorrecto(self):
        respuesta = self.client.post(self.url_login, {
            'username': 'admin_sgh',
            'password': 'contraseña_incorrecta',
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(respuesta.wsgi_request.user.is_authenticated)

    def test_01c_login_usuario_inexistente(self):
        respuesta = self.client.post(self.url_login, {
            'username': 'usuario_fantasma',
            'password': 'cualquier_clave',
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(respuesta.wsgi_request.user.is_authenticated)

    def test_01d_acceso_sin_sesion_redirige_a_login(self):
        respuesta = self.client.get(reverse('dashboard'))
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('/login/', respuesta['Location'])


# ===========================================================================
# TC-02: Registro de usuario
# ===========================================================================

class TC02_RegistroUsuario(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('registro')

    def test_02a_registro_usuario_valido(self):
        respuesta = self.client.post(self.url, {
            'username': 'nuevo_admin',
            'password1': 'Django2026@SGH',
            'password2': 'Django2026@SGH',
        })
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(User.objects.filter(username='nuevo_admin').exists())

    def test_02b_registro_passwords_no_coinciden(self):
        respuesta = self.client.post(self.url, {
            'username': 'otro_admin',
            'password1': 'Django2026@SGH',
            'password2': 'OtraClave123@',
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(User.objects.filter(username='otro_admin').exists())


# ===========================================================================
# TC-03: Crear paciente (vista HTML)
# ===========================================================================

class TC03_CrearPaciente(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='admin_sgh', password='SGH2026@seguro')
        self.client.login(username='admin_sgh', password='SGH2026@seguro')
        self.url = reverse('crear_paciente')

    def test_03a_crear_paciente_datos_validos(self):
        respuesta = self.client.post(self.url, PACIENTE_VALIDO)
        self.assertEqual(respuesta.status_code, 302)
        self.assertRedirects(respuesta, reverse('lista_pacientes'), fetch_redirect_response=False)
        self.assertTrue(Paciente.objects.filter(numero_documento='1234567890').exists())

    def test_03b_crear_paciente_documento_duplicado(self):
        Paciente.objects.create(**PACIENTE_VALIDO)
        datos = PACIENTE_VALIDO.copy()
        datos['correo'] = 'otro@email.com'
        respuesta = self.client.post(self.url, datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Paciente.objects.filter(numero_documento='1234567890').count(), 1)

    def test_03c_crear_paciente_campos_vacios(self):
        respuesta = self.client.post(self.url, {
            'tipo_documento': 'CC',
            'numero_documento': '',
            'nombres': '',
            'apellidos': '',
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Paciente.objects.count(), 0)

    def test_03d_correo_duplicado_muestra_advertencia(self):
        Paciente.objects.create(**PACIENTE_VALIDO)
        datos = PACIENTE_2.copy()
        datos['correo'] = PACIENTE_VALIDO['correo']
        respuesta = self.client.post(self.url, datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b'advertencia', respuesta.content.lower())


# ===========================================================================
# TC-04: Listado y paginacion
# ===========================================================================

class TC04_ListarPacientes(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='admin_sgh', password='SGH2026@seguro')
        self.client.login(username='admin_sgh', password='SGH2026@seguro')
        for i in range(6):
            Paciente.objects.create(
                tipo_documento='CC',
                numero_documento=f'100000{i:04d}',
                nombres=f'Paciente{i}',
                apellidos='Prueba',
                fecha_nacimiento='1990-01-01',
                telefono='3001234567',
                correo=f'paciente{i}@test.com',
                direccion=f'Calle {i}',
            )

    def test_04a_listado_visible_con_sesion(self):
        respuesta = self.client.get(reverse('lista_pacientes'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b'Paciente', respuesta.content)

    def test_04b_pagina_1_muestra_5_registros(self):
        respuesta = self.client.get(reverse('lista_pacientes') + '?page=1')
        self.assertEqual(len(respuesta.context['page_obj'].object_list), 5)

    def test_04c_pagina_2_muestra_1_registro(self):
        respuesta = self.client.get(reverse('lista_pacientes') + '?page=2')
        self.assertEqual(len(respuesta.context['page_obj'].object_list), 1)

    def test_04d_dashboard_total_correcto(self):
        respuesta = self.client.get(reverse('dashboard'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context['total_pacientes'], 6)


# ===========================================================================
# TC-05: Busqueda inteligente
# ===========================================================================

class TC05_BusquedaInteligente(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='admin_sgh', password='SGH2026@seguro')
        self.client.login(username='admin_sgh', password='SGH2026@seguro')
        self.p1 = Paciente.objects.create(**PACIENTE_VALIDO)
        self.p2 = Paciente.objects.create(**PACIENTE_2)
        self.p3 = Paciente.objects.create(**PACIENTE_3)

    def _buscar(self, termino):
        return self.client.get(reverse('lista_pacientes') + f'?buscar={termino}')

    def test_05a_busqueda_por_nombre(self):
        respuesta = self._buscar('Juan')
        resultados = list(respuesta.context['page_obj'].object_list)
        self.assertIn(self.p1, resultados)
        self.assertNotIn(self.p2, resultados)

    def test_05b_busqueda_nombre_orden_invertido(self):
        respuesta = self._buscar('Garcia Juan')
        resultados = list(respuesta.context['page_obj'].object_list)
        self.assertIn(self.p1, resultados)

    def test_05c_busqueda_por_apellido(self):
        respuesta = self._buscar('Rodriguez')
        resultados = list(respuesta.context['page_obj'].object_list)
        self.assertIn(self.p3, resultados)
        self.assertNotIn(self.p1, resultados)

    def test_05d_busqueda_por_documento(self):
        respuesta = self._buscar('9876543210')
        resultados = list(respuesta.context['page_obj'].object_list)
        self.assertIn(self.p2, resultados)

    def test_05e_busqueda_sin_coincidencia(self):
        respuesta = self._buscar('XxXNoExisteXxX')
        self.assertEqual(len(respuesta.context['page_obj'].object_list), 0)


# ===========================================================================
# TC-06: Editar paciente
# ===========================================================================

class TC06_EditarPaciente(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='admin_sgh', password='SGH2026@seguro')
        self.client.login(username='admin_sgh', password='SGH2026@seguro')
        self.paciente = Paciente.objects.create(**PACIENTE_VALIDO)
        self.url = reverse('editar_paciente', args=[self.paciente.id])

    def test_06a_editar_telefono(self):
        datos = PACIENTE_VALIDO.copy()
        datos['telefono'] = '3159999999'
        respuesta = self.client.post(self.url, datos)
        self.assertEqual(respuesta.status_code, 302)
        self.paciente.refresh_from_db()
        self.assertEqual(self.paciente.telefono, '3159999999')

    def test_06b_editar_id_inexistente_404(self):
        respuesta = self.client.get(reverse('editar_paciente', args=[99999]))
        self.assertEqual(respuesta.status_code, 404)

    def test_06c_formulario_precompletado(self):
        respuesta = self.client.get(self.url)
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, '1234567890')


# ===========================================================================
# TC-07: Eliminar paciente
# ===========================================================================

class TC07_EliminarPaciente(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='admin_sgh', password='SGH2026@seguro')
        self.client.login(username='admin_sgh', password='SGH2026@seguro')
        self.paciente = Paciente.objects.create(**PACIENTE_VALIDO)
        self.url = reverse('eliminar_paciente', args=[self.paciente.id])

    def test_07a_get_muestra_confirmacion(self):
        respuesta = self.client.get(self.url)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(Paciente.objects.filter(id=self.paciente.id).exists())

    def test_07b_post_elimina_paciente(self):
        respuesta = self.client.post(self.url)
        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(Paciente.objects.filter(id=self.paciente.id).exists())

    def test_07c_eliminar_inexistente_404(self):
        respuesta = self.client.post(reverse('eliminar_paciente', args=[99999]))
        self.assertEqual(respuesta.status_code, 404)


# ===========================================================================
# TC-08: API REST — Autenticacion con Token
# ===========================================================================

class TC08_APIAutenticacion(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.usuario = User.objects.create_user(
            username='api_user', password='APIpass2026@'
        )
        self.url_login = reverse('api_login')

    def test_08a_login_api_retorna_token(self):
        respuesta = self.client.post(self.url_login, {
            'username': 'api_user',
            'password': 'APIpass2026@',
        }, format='json')
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('token', respuesta.data)

    def test_08b_login_api_credenciales_incorrectas(self):
        respuesta = self.client.post(self.url_login, {
            'username': 'api_user',
            'password': 'ClaveEquivocada',
        }, format='json')
        self.assertEqual(respuesta.status_code, 401)

    def test_08c_acceso_sin_token_denegado(self):
        respuesta = self.client.get(reverse('api_pacientes'))
        self.assertIn(respuesta.status_code, [401, 403])

    def test_08d_endpoint_me_retorna_datos(self):
        token = Token.objects.create(user=self.usuario)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        respuesta = self.client.get(reverse('api_me'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data['username'], 'api_user')


# ===========================================================================
# TC-09: API REST — CRUD de pacientes
# ===========================================================================

class TC09_APICRUDPacientes(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.usuario = User.objects.create_user(
            username='api_user', password='APIpass2026@'
        )
        self.token = Token.objects.create(user=self.usuario)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.paciente = Paciente.objects.create(**PACIENTE_VALIDO)
        self.url_lista = reverse('api_pacientes')
        self.url_detalle = reverse('api_paciente_detail', args=[self.paciente.id])

    def test_09a_get_listado_paginado(self):
        respuesta = self.client.get(self.url_lista)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('count', respuesta.data)
        self.assertIn('results', respuesta.data)
        self.assertEqual(respuesta.data['count'], 1)

    def test_09b_post_crear_paciente(self):
        respuesta = self.client.post(self.url_lista, PACIENTE_2, format='json')
        self.assertEqual(respuesta.status_code, 201)
        self.assertTrue(Paciente.objects.filter(numero_documento='9876543210').exists())

    def test_09c_get_detalle_paciente(self):
        respuesta = self.client.get(self.url_detalle)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data['numero_documento'], '1234567890')

    def test_09d_put_actualizar_completo(self):
        datos = PACIENTE_VALIDO.copy()
        datos['telefono'] = '3001111111'
        respuesta = self.client.put(self.url_detalle, datos, format='json')
        self.assertEqual(respuesta.status_code, 200)
        self.paciente.refresh_from_db()
        self.assertEqual(self.paciente.telefono, '3001111111')

    def test_09e_patch_actualizar_parcial(self):
        respuesta = self.client.patch(
            self.url_detalle, {'direccion': 'Nueva Direccion 123'}, format='json'
        )
        self.assertEqual(respuesta.status_code, 200)
        self.paciente.refresh_from_db()
        self.assertEqual(self.paciente.direccion, 'Nueva Direccion 123')
        self.assertEqual(self.paciente.nombres, 'Juan')

    def test_09f_delete_eliminar(self):
        respuesta = self.client.delete(self.url_detalle)
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Paciente.objects.filter(id=self.paciente.id).exists())

    def test_09g_post_documento_duplicado_400(self):
        datos = PACIENTE_2.copy()
        datos['numero_documento'] = '1234567890'
        respuesta = self.client.post(self.url_lista, datos, format='json')
        self.assertEqual(respuesta.status_code, 400)

    def test_09h_busqueda_via_api(self):
        Paciente.objects.create(**PACIENTE_2)
        respuesta = self.client.get(self.url_lista + '?buscar=Juan')
        self.assertEqual(respuesta.status_code, 200)
        numeros = [p['numero_documento'] for p in respuesta.data['results']]
        self.assertIn('1234567890', numeros)
        self.assertNotIn('9876543210', numeros)


# ===========================================================================
# TC-10: Modelo de datos — integridad
# ===========================================================================

class TC10_ModeloPaciente(TestCase):
    def test_10a_crear_paciente_persiste(self):
        p = Paciente.objects.create(**PACIENTE_VALIDO)
        self.assertEqual(Paciente.objects.count(), 1)
        self.assertEqual(p.nombres, 'Juan')

    def test_10b_numero_documento_unico(self):
        from django.db import IntegrityError
        Paciente.objects.create(**PACIENTE_VALIDO)
        with self.assertRaises(IntegrityError):
            Paciente.objects.create(**PACIENTE_VALIDO)

    def test_10c_str_incluye_identificadores(self):
        p = Paciente.objects.create(**PACIENTE_VALIDO)
        cadena = str(p)
        self.assertIn('CC', cadena)
        self.assertIn('1234567890', cadena)

    def test_10d_fecha_registro_automatica(self):
        p = Paciente.objects.create(**PACIENTE_VALIDO)
        self.assertIsNotNone(p.fecha_registro)
