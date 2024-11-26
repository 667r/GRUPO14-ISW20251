from django.shortcuts import render
from django.http import HttpResponse
from .models import Boletin
from django.db.models import Q
from django import forms
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

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