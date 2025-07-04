from django.urls import path
from . import views
from .views import api_fuentes
from .views import backup_manual_view, logout_view, acceso_denegado
from .views import api_ping
from .views import api_boletines

urlpatterns = [
    path('', views.index, name='index'),
    path('api/ping/', api_ping),
    path('api/fuentes/', api_fuentes, name='api_fuentes'),
    path('api/boletines/', api_boletines, name='api_boletines'),
    path('boletines/', views.boletines, name='boletines'),
    path('crear-boletin/', views.crear_boletin, name='crear_boletin'),
    path('login/', views.login_view, name='login'),  # Página de inicio de sesión
    path('signup/', views.signup, name='signup'),  # Página de creación de cuenta
    path('fuentes/vista/<int:fuente_id>/', views.vista_csv, name='vista_csv'),
    path('fuentes/', views.listar_fuentes, name='listar_fuentes'),
    path('fuentes/nueva/', views.crear_fuente, name='crear_fuente'),
    path('fuentes/eliminar/<int:fuente_id>/', views.eliminar_fuente, name='eliminar_fuente'),
    path('backup/manual/', views.backup_manual_view, name='backup_manual'),
    path('logout/', logout_view, name='logout'),
    path('acceso-denegado/', acceso_denegado, name='acceso_denegado'),

]

