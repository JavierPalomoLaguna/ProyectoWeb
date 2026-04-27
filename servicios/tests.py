from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Reserva


# ---------------------------------------------------------------------------
# Tests del modelo Reserva
# ---------------------------------------------------------------------------

class ReservaModelTest(TestCase):

    def setUp(self):
        self.reserva = Reserva.objects.create(
            nombre='Ana García',
            telefono='600123456',
            email='ana@example.com',
            fecha='2026-06-15',
            hora='20:30',
            numero_personas=4,
            comentarios='Mesa cerca de la ventana',
        )

    def test_estado_por_defecto_es_pendiente(self):
        """Una reserva nueva debe crearse con estado 'pendiente'."""
        self.assertEqual(self.reserva.estado, 'pendiente')

    def test_str_contiene_nombre_y_fecha(self):
        """El __str__ debe incluir el nombre del cliente y la fecha."""
        texto = str(self.reserva)
        self.assertIn('Ana García', texto)
        self.assertIn('2026-06-15', texto)

    def test_campos_obligatorios_se_guardan(self):
        """Todos los campos enviados deben persistir correctamente."""
        r = Reserva.objects.get(pk=self.reserva.pk)
        self.assertEqual(r.telefono, '600123456')
        self.assertEqual(r.numero_personas, 4)
        self.assertEqual(r.comentarios, 'Mesa cerca de la ventana')


# ---------------------------------------------------------------------------
# Tests de la vista procesar_reserva
# ---------------------------------------------------------------------------

class ProcesarReservaViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('procesar_reserva')
        self.datos_validos = {
            'nombre': 'Carlos López',
            'telefono': '611222333',
            'email': 'carlos@example.com',
            'fecha': '2026-07-20',
            'hora': '21:00',
            'numero_personas': '2',
            'comentarios': 'Sin gluten por favor',
        }

    def test_reserva_correcta_se_guarda_en_bd(self):
        """Un POST con datos válidos debe crear exactamente una reserva en BD."""
        self.client.post(self.url, self.datos_validos)
        self.assertEqual(Reserva.objects.count(), 1)

    def test_reserva_correcta_guarda_datos_correctos(self):
        """Los datos guardados deben coincidir con los enviados."""
        self.client.post(self.url, self.datos_validos)
        reserva = Reserva.objects.first()
        self.assertEqual(reserva.nombre, 'Carlos López')
        self.assertEqual(reserva.email, 'carlos@example.com')
        self.assertEqual(reserva.numero_personas, 2)
        self.assertEqual(reserva.estado, 'pendiente')

    def test_reserva_correcta_redirige_a_servicios(self):
        """Tras una reserva válida, debe redirigir a /servicios/."""
        response = self.client.post(self.url, self.datos_validos)
        self.assertRedirects(response, '/servicios/#reservas')

    def test_reserva_correcta_genera_mensaje_exito(self):
        """Una reserva válida debe dejar un mensaje de éxito en la sesión."""
        response = self.client.post(self.url, self.datos_validos, follow=True)
        mensajes = list(get_messages(response.wsgi_request))
        self.assertTrue(any('correctamente' in str(m) for m in mensajes))

    def test_campos_faltantes_no_crean_reserva(self):
        """Un POST sin campos obligatorios no debe crear ninguna reserva."""
        datos_incompletos = {
            'nombre': 'Sin Email',
            'telefono': '600000000',
            # email ausente
            'fecha': '2026-07-20',
            'hora': '21:00',
            'numero_personas': '3',
        }
        self.client.post(self.url, datos_incompletos)
        self.assertEqual(Reserva.objects.count(), 0)

    def test_campos_faltantes_generan_mensaje_error(self):
        """Un POST incompleto debe generar un mensaje de error."""
        datos_incompletos = {'nombre': 'Incompleto'}
        response = self.client.post(self.url, datos_incompletos, follow=True)
        mensajes = list(get_messages(response.wsgi_request))
        self.assertTrue(any('obligatorios' in str(m) for m in mensajes))

    def test_get_redirige_a_servicios(self):
        """Una petición GET a procesar_reserva debe redirigir a /servicios/."""
        response = self.client.get(self.url)
        self.assertRedirects(response, '/servicios/')