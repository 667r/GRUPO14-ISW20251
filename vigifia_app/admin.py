from django.contrib import admin
from .models import Boletin

class BoletinAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'categoria', 'ubicacion')
    list_filter = ('categoria', 'ubicacion', 'fecha')
    search_fields = ('titulo', 'tipo')
    date_hierarchy = 'fecha'

admin.site.register(Boletin, BoletinAdmin)