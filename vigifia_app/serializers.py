from rest_framework import serializers
from .models import FuenteExterna
from .models import Boletin

class FuenteExternaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuenteExterna
        fields = '__all__'

#para pruebas unitarias hito 3.
class BoletinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boletin
        fields = ['id', 'titulo', 'fecha', 'tipo', 'categoria', 'ubicacion']  # ajusta según campos relevantes