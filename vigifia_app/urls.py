from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('boletines/', views.boletines, name='boletines'),
    path('crear-boletin/', views.crear_boletin, name='crear_boletin'),
    path('login/', views.login_view, name='login'),  # Página de inicio de sesión
    path('signup/', views.signup, name='signup'),  # Página de creación de cuenta
]

