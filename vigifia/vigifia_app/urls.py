from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('boletines/', views.boletines, name='boletines'),
    path('crear-boletin/', views.crear_boletin, name='crear_boletin'),
]

