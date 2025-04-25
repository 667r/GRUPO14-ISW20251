from django.urls import path
from . import views
from .views import api_fuentes
from vigifia_app.views import api_ping

urlpatterns = [
    path('', views.index, name='index'),
    path('api/ping/', api_ping),
    path('api/fuentes/', api_fuentes, name='api_fuentes'),
    path('boletines/', views.boletines, name='boletines'),
    path('crear-boletin/', views.crear_boletin, name='crear_boletin'),
    path('login/', views.login_view, name='login'),  # Página de inicio de sesión
    path('signup/', views.signup, name='signup'),  # Página de creación de cuenta
    path('media/fuentes/vista/<int:fuente_id>/', views.vista_csv, name='vista_csv'),
    path('fuentes/', views.listar_fuentes, name='listar_fuentes'),
    path('fuentes/nueva/', views.crear_fuente, name='crear_fuente'),
    path('fuentes/eliminar/<int:fuente_id>/', views.eliminar_fuente, name='eliminar_fuente'),

]

