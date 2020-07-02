from django.contrib import admin

# Register your models here.
from apps.abastecimiento.models import Pedido, DetallePedido


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'estado', 'format_fecha', 'total', 'tipo_documento', 'tipo_pago', 'proveedor',
                    'usuario')
    search_fields = ('id', 'numero')
    list_filter = ('estado', 'fecha')
    ordering = ('-id',)

    def format_fecha(self, obj):
        return obj.fecha.strftime("%d/%m/%Y %H:%M:%S")

    format_fecha.short_description = 'Fecha'
    format_fecha.admin_order_field = 'fecha'


class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'producto', 'precio', 'cantidad', 'total')
    search_fields = ('id', 'pedido', 'pedido__numero')
    ordering = ('-id',)


admin.site.register(Pedido, PedidoAdmin)
admin.site.register(DetallePedido, DetallePedidoAdmin)
