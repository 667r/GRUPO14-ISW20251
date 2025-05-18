from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Boletin
from .serializers import BoletinSerializer
from django.db.models import Q
from django import forms
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import FuenteExternaForm
from .models import FuenteExterna
import csv
from django.contrib import messages
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FuenteExternaSerializer
import subprocess
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils.timezone import now
import os
from datetime import datetime



@api_view(['GET'])
def api_fuentes(request):
    fuentes = FuenteExterna.objects.all()
    serializer = FuenteExternaSerializer(fuentes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_ping(request):
    return Response({"message": "Hola desde Django 👋"})

#endpoint agregado para pruebas unitarias hito 3
@api_view(['GET'])
def api_boletines(request):
    boletines = Boletin.objects.all().order_by('-fecha')
    serializer = BoletinSerializer(boletines, many=True)
    return Response(serializer.data)

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Redirigir a la página principal
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vista para registrarse
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirigir a la página principal
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def boletines(request):
    boletines = Boletin.objects.all().order_by('-fecha')
    
    categoria = request.GET.get('categoria')
    fecha = request.GET.get('fecha')
    ubicacion = request.GET.get('ubicacion')

    if categoria and categoria != 'Seleccionar Categoría':
        boletines = boletines.filter(categoria=categoria)
    
    if fecha:
        boletines = boletines.filter(fecha=fecha)
    
    if ubicacion and ubicacion != 'Seleccionar Ubicación':
        boletines = boletines.filter(ubicacion=ubicacion)

    categorias = Boletin.objects.values_list('categoria', flat=True).distinct()
    ubicaciones = Boletin.objects.values_list('ubicacion', flat=True).distinct()

    context = {
        'boletines': boletines,
        'categorias': categorias,
        'ubicaciones': ubicaciones,
        'selected_categoria': categoria,
        'selected_fecha': fecha,
        'selected_ubicacion': ubicacion,
    }

    return render(request, 'boletines.html', context)

class BoletinForm(forms.ModelForm):
    class Meta:
        model = Boletin
        fields = ['titulo', 'foto', 'fecha', 'tipo', 'categoria', 'ubicacion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

def crear_boletin(request):
    if request.method == 'POST':
        form = BoletinForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Boletín creado exitosamente.')
            return redirect('boletines')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = BoletinForm()
    return render(request, 'crear_boletin.html', {'form': form})

def vista_csv(request, fuente_id):
    fuente = get_object_or_404(FuenteExterna, id=fuente_id)
    if fuente.archivo_csv and fuente.tipo == 'csv':
        try:
            df = pd.read_csv(fuente.archivo_csv.path)
            headers = df.columns.tolist()
            rows = df.values.tolist()
            context = {
                'fuente': fuente,
                'headers': headers,
                'rows': rows
            }
            return render(request, 'vista_csv.html', context)
        except Exception as e:
            return render(request, 'vista_csv.html', {'error': str(e)})
    else:
        return render(request, 'vista_csv.html', {'error': 'No es un archivo CSV válido.'})
    
def listar_fuentes(request):
    fuentes = FuenteExterna.objects.all().order_by('-fecha_subida')
    return render(request, 'listar_fuentes.html', {'fuentes': fuentes})

def crear_fuente(request):
    if request.method == 'POST':
        form = FuenteExternaForm(request.POST, request.FILES)
        if form.is_valid():
            fuente = form.save(commit=False)
            fuente.usuario = request.user
            fuente.save()
            messages.success(request, "Fuente agregada exitosamente.")
            return redirect('listar_fuentes')
    else:
        form = FuenteExternaForm()
    return render(request, 'crear_fuente.html', {'form': form})

def eliminar_fuente(request, fuente_id):
    fuente = get_object_or_404(FuenteExterna, id=fuente_id)
    fuente.delete()
    messages.success(request, "Fuente eliminada.")
    return redirect('listar_fuentes')

@staff_member_required   
def backup_manual_view(request):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/app/backups/manual_backup_{now}.sql"

    try:
        result = subprocess.run(
            [
                "pg_dump",
                "-h", "db",
                "-U", "equipo",
                "-d", "isw",
                "-f", filename
            ],
            env={**os.environ, "PGPASSWORD": "equipo123"},  # ⚠️ aquí pones tu password de DB
            check=True
        )
        with open(filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/sql')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
            return response
    except Exception as e:
        return HttpResponse(f"Error al generar backup: {e}")