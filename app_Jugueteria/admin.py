from django.contrib import admin
from django.utils.html import format_html
from .models import Sucursal, Cliente, Empleado

# ==========================
# ADMIN: Sucursal
# ==========================
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'ciudad', 'estado', 'thumbnail')
    readonly_fields = ('thumbnail',)

    def thumbnail(self, obj):
        if hasattr(obj, 'imagen') and obj.imagen:
            return format_html('<img src="{}" style="max-width:120px;"/>', obj.imagen.url)
        return '-'
    thumbnail.short_description = 'Imagen'

# ==========================
# ADMIN: Empleado
# ==========================
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'edad', 'puesto', 'salario', 'id_sucursal')
    search_fields = ('nombre', 'apellido', 'puesto')
    list_filter = ('id_sucursal', 'puesto')

admin.site.register(Sucursal, SucursalAdmin)
admin.site.register(Cliente)
admin.site.register(Empleado, EmpleadoAdmin)

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'edad', 'telefono', 'email', 'id_sucursal')
    search_fields = ('nombre', 'apellido', 'telefono', 'email')
    list_filter = ('id_sucursal',)
