from apps.cmp.models import venta
from django.contrib import admin


class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'carrito', 'estado', 'format_fecha', 'tipo_despacho', 'precio', 'ciudad', 'comuna',
                    'cli_apellidos', 'cli_nombres', 'cli_rut', 'cli_empresa')
    search_fields = ('id', 'cli_rut')
    list_filter = ('estado', 'fc')
    ordering = ('-id',)

    def format_fecha(self, obj):
        return obj.fc.strftime("%d/%m/%Y %H:%M:%S")

    format_fecha.short_description = 'Fecha'
    format_fecha.admin_order_field = 'fecha'


admin.site.register(venta, VentaAdmin)
