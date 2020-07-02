from django.contrib import admin

from .models import Carrito, CarritoProducto, Categoria, Producto, TipoProducto, Marca


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'Nombre', 'descripcion', 'marca', 'color', 'precio', 'stock',
                    'Categoria', 'TipoProducto')
    search_fields = ('id', 'Nombre', 'codigo')
    # list_filter = ('estado', 'fecha')
    ordering = ('-codigo',)


admin.site.register(Categoria)
admin.site.register(TipoProducto)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Carrito)
admin.site.register(CarritoProducto)
admin.site.register(Marca)
