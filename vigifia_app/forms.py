
from django import forms
from .models import FuenteExterna

class FuenteExternaForm(forms.ModelForm):
    class Meta:
        model = FuenteExterna
        fields = ['tipo', 'archivo_csv', 'url_api', 'nombre', 'descripcion']

