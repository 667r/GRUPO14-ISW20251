from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Boletin
from .serializers import BoletinSerializer
from django.db.models import Q
from django import forms
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import FuenteExternaForm
from .models import FuenteExterna
from django.contrib.auth.decorators import login_required, user_passes_test
import csv
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FuenteExternaSerializer
import subprocess
from django.contrib.admin.views.decorators import staff_member_required
from vigifia_app.services.data_ingestion import CSVSourceHandler, APISourceHandler
from django.http import HttpResponse
from django.utils.timezone import now
import os
from datetime import datetime
import requests
from django.core.exceptions import ValidationError
import json
from vigifia_app.utils.backup import generate_backup, restore_backup
import logging



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
    return render(request, 'index.html', {})

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

@login_required
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

    if fuente.tipo == 'csv':
        handler = CSVSourceHandler(fuente)
    elif fuente.tipo == 'api':
        handler = APISourceHandler(fuente)
    else:
        return render(request, 'vista_csv.html', {'error': 'Tipo de fuente no soportado.'})

    try:
        data = handler.ingest()
        fuente.contenido = data
        fuente.save()

        # Si es una API con imagen simple
        if fuente.tipo == 'api' and isinstance(data, dict) and 'message' in data:
            return render(request, 'vista_csv.html', {
                'fuente': fuente,
                'imagen_url': data['message']
            })

        # Si la respuesta es un diccionario con una lista de elementos
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                    headers = value[0].keys() if value else []
                    rows = [item.values() for item in value]
                    return render(request, 'vista_csv.html', {
                        'fuente': fuente,
                        'headers': headers,
                        'rows': rows,
                        'table_title': key,
                    })

        # Si es una lista de diccionarios simple
        if isinstance(data, list) and all(isinstance(d, dict) for d in data):
            headers = data[0].keys() if data else []
            rows = [d.values() for d in data]
            return render(request, 'vista_csv.html', {
                'fuente': fuente,
                'headers': headers,
                'rows': rows
            })

        # Mostrar como JSON plano si no se puede estructurar en tabla
        return render(request, 'vista_csv.html', {
            'fuente': fuente,
            'json_content': json.dumps(data, indent=2)
        })

    except Exception as e:
        return render(request, 'vista_csv.html', {'error': str(e)})

@login_required   
def listar_fuentes(request):
    fuentes = FuenteExterna.objects.all().order_by('-fecha_subida')
    return render(request, 'listar_fuentes.html', {'fuentes': fuentes})


@login_required 
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

# Logging
logging.basicConfig(filename='/app/backups/backup.log', level=logging.INFO)

def log_backup(status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Backup realizado a las {timestamp} con estado: {status}")
# ---
@staff_member_required   
def backup_manual_view(request):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/app/backups/manual_backup_{now}.sql"

    try:
        # Ejecutar el comando de backup
        result = subprocess.run(
            [
                "pg_dump",
                "-h", "db",
                "-U", "equipo",
                "-d", "isw",
                "-f", filename
            ],
            env={**os.environ, "PGPASSWORD": "equipo123"},  # ⚠️ Aquí pon tu password de DB
            check=True
        )
        
        # Guardar el archivo de backup
        with open(filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/sql')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'

        # Log de éxito
        log_backup('Éxito')
        
        # Notificación visual de éxito en el admin
        messages.success(request, f"Backup realizado con éxito a las {now}")
        
        return response
    
    except Exception as e:
        # Log de error
        log_backup(f'Error: {str(e)}')
        
        # Notificación visual de error en el admin
        messages.error(request, f"Error al generar backup: {str(e)}")
        
        return HttpResponse(f"Error al generar backup: {str(e)}")
    
    
@login_required
@user_passes_test(lambda u: u.is_superuser)
def restaurar_backup_view(request):
    filename = request.POST.get('backup_file')
    if filename:
        success = restore_backup(filename)
        if success:
            messages.success(request, f"Backup restaurado correctamente desde {filename}")
        else:
            messages.error(request, "Error al restaurar el backup.")
    else:
        messages.error(request, "Debe especificar un archivo de respaldo.")
    return redirect('admin:index')

def logout_view(request):
    logout(request)
    return redirect('/')  # Redirige al inicio tras cerrar sesión


def acceso_denegado(request):
    return render(request, 'acceso_denegado.html', status=403)