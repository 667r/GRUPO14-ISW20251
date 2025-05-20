from django.test import TestCase, Client
from rest_framework import status
from vigifia_app.models import FuenteExterna, Boletin
from vigifia_app.serializers import FuenteExternaSerializer
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient 

# Test para /api/ping/
class ApiPingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        usuario = User.objects.create_user(username='testuser', password='12345')
        FuenteExterna.objects.create(
            nombre='Fuente Test',
            tipo='api',
            usuario=usuario,
            url_api='http://test.com'
        )

    def test_get_ping_returns_200(self):
        response = self.client.get('/api/ping/')
        print("\n[GET /ping/] ->", response.status_code, response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hola desde Django 👋"})

    def test_post_ping_returns_405(self):
        response = self.client.post('/api/ping/')
        print("\n[POST /ping/] ->", response.status_code)
        self.assertEqual(response.status_code, 405)

# Test para /api/fuentes/
class ApiFuentesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        usuario = User.objects.create_user(username='testuser', password='12345')
        FuenteExterna.objects.create(
            nombre='Fuente Test',
            tipo='api',
            usuario=usuario,
            url_api='http://test.com'
        )

    def test_get_fuentes_returns_data_when_exist(self):
        response = self.client.get('/api/fuentes/')
        print("\n[GET /fuentes/ con datos] ->", response.status_code, response.json())
        fuentes = FuenteExterna.objects.all()
        serializer = FuenteExternaSerializer(fuentes, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), serializer.data)

    def test_get_fuentes_returns_empty_when_none(self):
        FuenteExterna.objects.all().delete()
        response = self.client.get('/api/fuentes/')
        print("\n[GET /fuentes/ vacío] ->", response.status_code, response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

# Test para /api/boletines/
class ApiBoletinesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        Boletin.objects.create(titulo='Boletin 1', fecha='2024-01-01', tipo='Info', categoria='Cat1', ubicacion='Loc1')
        Boletin.objects.create(titulo='Boletin 2', fecha='2024-01-02', tipo='Aviso', categoria='Cat2', ubicacion='Loc2')

    def test_get_boletines_returns_data(self):
        url = reverse('api_boletines')
        response = self.client.get(url)
        print("\n[GET /boletines/ con datos] ->", response.status_code, response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['titulo'], 'Boletin 2')

    def test_get_boletines_returns_empty_list(self):
        Boletin.objects.all().delete()
        url = reverse('api_boletines')
        response = self.client.get(url)
        print("\n[GET /boletines/ vacío] ->", response.status_code, response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
