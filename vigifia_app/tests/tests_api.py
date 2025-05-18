from django.test import TestCase, Client
from rest_framework import status
from vigifia_app.models import FuenteExterna, Boletin  # Ajusta según tu proyecto
from vigifia_app.serializers import FuenteExternaSerializer
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient 

#test simple, no crucial
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

#test simple2, no crucial
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

#prueba untaria básica,
class ApiBoletinesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        # Crear boletines de prueba
        Boletin.objects.create(titulo='Boletin 1', fecha='2024-01-01', tipo='Info', categoria='Cat1', ubicacion='Loc1')
        Boletin.objects.create(titulo='Boletin 2', fecha='2024-01-02', tipo='Aviso', categoria='Cat2', ubicacion='Loc2')

    def test_get_boletines(self):
        url = reverse('api_boletines')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['titulo'], 'Boletin 2')  # orden descendente por fecha