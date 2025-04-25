from rest_framework import serializers
from .models import FuenteExterna

class FuenteExternaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuenteExterna
        fields = '__all__'