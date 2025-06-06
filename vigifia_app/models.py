from django.db import models
from django.contrib.auth.models import User

class FuenteExterna(models.Model):
    TIPO_CHOICES = [
        ('csv', 'Archivo CSV'),
        ('api', 'API Externa'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    archivo_csv = models.FileField(upload_to='fuentes/', blank=True, null=True)
    nombre = models.CharField(max_length=100)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    url_api = models.URLField(blank=True, null=True)
    contenido = models.JSONField(blank=True, null=True)
    


    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
    
class Boletin(models.Model):
    CATEGORIAS = [
        ('Cambio climático', 'Cambio climático'),
        ('Recursos hídricos', 'Recursos hídricos'),
        ('Sistemas alimentarios', 'Sistemas alimentarios'),
    ]
    
    UBICACIONES = [
        ('Región Metropolitana', 'Región Metropolitana'),
        ('Valparaíso', 'Valparaíso'),
        ('Biobío', 'Biobío'),
        ('Los Lagos', 'Los Lagos'),
        ('Araucanía', 'Araucanía'),
        ('Coquimbo', 'Coquimbo'),
        ('Antofagasta', 'Antofagasta'),
        ('O´Higgins', 'O´Higgins'),
        ('Maule', 'Maule'),
        ('Atacama', 'Atacama'),
        ('Los Ríos', 'Los Ríos'),
        ('Ñuble', 'Ñuble'),
        ('Tarapacá', 'Tarapacá'),
        ('Aysén', 'Aysén'),
        ('Magallanes', 'Magallanes'),
        ('Arica y Parinacota', 'Arica y Parinacota'),
    ]

    titulo = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='boletines/')
    fecha = models.DateField()
    tipo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=40, choices=CATEGORIAS)
    ubicacion = models.CharField(max_length=50, choices=UBICACIONES)

    def __str__(self):
        return self.titulo