from django.contrib import admin
from .models import Boletin
from .models import FuenteExterna

class BoletinAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'categoria', 'ubicacion')
    list_filter = ('categoria', 'ubicacion', 'fecha')
    search_fields = ('titulo', 'tipo')
    date_hierarchy = 'fecha'

admin.site.register(Boletin, BoletinAdmin)

@admin.register(FuenteExterna)
class FuenteExternaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "fecha_subida")
    readonly_fields = ("contenido",)