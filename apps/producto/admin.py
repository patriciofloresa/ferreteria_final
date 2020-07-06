from django.contrib import admin

from .models import Carrito, CarritoProducto, Categoria, Producto, TipoProducto, Marca


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'Nombre', 'descripcion', 'marca', 'color', 'precio', 'stock',
                    'Categoria', 'TipoProducto')
    search_fields = ('id', 'Nombre', 'codigo')
    # list_filter = ('estado', 'fecha')
    ordering = ('-codigo',)


class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estatus', 'get_cant_items', 'monto_total')
    search_fields = ('id', 'usuario')
    list_filter = ('estatus', )
    ordering = ('-id',)

    def get_cant_items(self, obj):
        return obj.detalles.count() if obj.detalles else 0

    get_cant_items.short_description = 'Cant Items'


class CarritoProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'carrito', 'carrito_user', 'producto', 'producto_codigo', 'cantidad')
    search_fields = ('id', 'carrito', 'producto__codigo')
    ordering = ('-id',)

    def carrito_user(self, obj):
        return obj.carrito.usuario if obj.carrito else ''

    def producto_codigo(self, obj):
        return obj.producto.codigo if obj.producto else ''

    producto_codigo.short_description = 'prod codigo'
    producto_codigo.admin_order_field = 'producto__codigo'
    carrito_user.short_description = 'usuario carrito'
    carrito_user.admin_order_field = 'carrito__usuario'


admin.site.register(Categoria)
admin.site.register(TipoProducto)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(CarritoProducto, CarritoProductoAdmin)
admin.site.register(Marca)
