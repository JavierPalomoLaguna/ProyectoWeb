from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from .models import MensajeContacto


# ---------------------------------------------------------------------------
# Tests del modelo MensajeContacto
# ---------------------------------------------------------------------------

class MensajeContactoModelTest(TestCase):

    def setUp(self):
        self.mensaje = MensajeContacto.objects.create(
            nombre='Laura Sánchez',
            email='laura@example.com',
            contenido='Me gustaría saber más sobre sus servicios.',
        )

    def test_str_contiene_nombre_y_email(self):
        """El __str__ debe incluir nombre e email."""
        texto = str(self.mensaje)
        self.assertIn('Laura Sánchez', texto)
        self.assertIn('laura@example.com', texto)

    def test_campos_se_guardan_correctamente(self):
        """Los campos enviados deben persistir en BD."""
        m = MensajeContacto.objects.get(pk=self.mensaje.pk)
        self.assertEqual(m.nombre, 'Laura Sánchez')
        self.assertEqual(m.contenido, 'Me gustaría saber más sobre sus servicios.')


# ---------------------------------------------------------------------------
# Tests de la vista contacto
# ---------------------------------------------------------------------------

class ContactoViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('contacto')
        self.datos_validos = {
            'name': 'Pedro Martín',
            'email': 'pedro@example.com',
            'contenido': 'Quiero solicitar presupuesto para una tienda online.',
        }

    def test_get_devuelve_200(self):
        """La página de contacto debe responder con código 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_valido_guarda_mensaje_en_bd(self):
        """Un POST válido debe crear exactamente un MensajeContacto en BD."""
        self.client.post(self.url, self.datos_validos)
        self.assertEqual(MensajeContacto.objects.count(), 1)

    def test_post_valido_guarda_datos_correctos(self):
        """Los datos guardados deben coincidir con los enviados."""
        self.client.post(self.url, self.datos_validos)
        mensaje = MensajeContacto.objects.first()
        self.assertEqual(mensaje.nombre, 'Pedro Martín')
        self.assertEqual(mensaje.email, 'pedro@example.com')

    def test_post_valido_envia_email(self):
        """Un POST válido debe disparar exactamente un email."""
        self.client.post(self.url, self.datos_validos)
        self.assertEqual(len(mail.outbox), 1)

    def test_email_enviado_tiene_asunto_correcto(self):
        """El email enviado debe tener el asunto esperado."""
        self.client.post(self.url, self.datos_validos)
        self.assertIn('contacto', mail.outbox[0].subject.lower())

    def test_email_contiene_nombre_remitente(self):
        """El cuerpo del email debe incluir el nombre del remitente."""
        self.client.post(self.url, self.datos_validos)
        self.assertIn('Pedro Martín', mail.outbox[0].body)

    def test_post_valido_muestra_mensaje_exito(self):
        """Tras un envío válido, la respuesta debe contener el mensaje de éxito."""
        response = self.client.post(self.url, self.datos_validos)
        self.assertContains(response, 'Mensaje enviado correctamente')

    def test_post_invalido_no_guarda_en_bd(self):
        """Un POST con email inválido no debe guardar nada en BD."""
        datos_malos = {
            'name': 'Sin Email',
            'email': 'esto-no-es-un-email',
            'contenido': 'Prueba.',
        }
        self.client.post(self.url, datos_malos)
        self.assertEqual(MensajeContacto.objects.count(), 0)

    def test_post_invalido_no_envia_email(self):
        """Un formulario inválido no debe enviar ningún email."""
        datos_malos = {
            'name': '',
            'email': 'noesvalido',
            'contenido': '',
        }
        self.client.post(self.url, datos_malos)
        self.assertEqual(len(mail.outbox), 0)