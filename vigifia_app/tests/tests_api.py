from django.test import TestCase, Client
from rest_framework import status
from vigifia_app.models import FuenteExterna  # Ajusta según tu proyecto
from vigifia_app.serializers import FuenteExternaSerializer
from django.contrib.auth.models import User

class ApiPingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        # Crear un usuario necesario para el FK 'usuario'
        usuario = User.objects.create_user(username='testuser', password='12345')

        FuenteExterna.objects.create(
            nombre='Fuente Test',
            tipo='api',  # uno de los valores válidos para TIPO_CHOICES
            usuario=usuario,
            url_api='http://test.com'
        )

    def test_get_ping(self):
        response = self.client.get('/api/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hola desde Django 👋"})

    def test_post_ping_not_allowed(self):
        response = self.client.post('/api/ping/')
        self.assertEqual(response.status_code, 405)

class ApiFuentesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        # Crear un usuario necesario para el FK 'usuario'
        usuario = User.objects.create_user(username='testuser', password='12345')

        FuenteExterna.objects.create(
            nombre='Fuente Test',
            tipo='api',  # uno de los valores válidos para TIPO_CHOICES
            usuario=usuario,
            url_api='http://test.com'
        )

    def test_get_fuentes_with_data(self):
        response = self.client.get('/api/fuentes/')
        fuentes = FuenteExterna.objects.all()
        serializer = FuenteExternaSerializer(fuentes, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), serializer.data)

    def test_get_fuentes_empty(self):
        FuenteExterna.objects.all().delete()  # borrar todas las fuentes
        response = self.client.get('/api/fuentes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
