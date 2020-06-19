from django.db import models
from apps.bases.models import ClaseModelo
from django.contrib.auth.models import User
from django.conf import settings
from apps.producto.models import Producto, CarritoProducto, Categoria, Carrito

# Create your models here.

""" class Venta(ClaseModelo):
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    id_venta
    Total
    Id_tipo_Usuario
    Comuna
    Direccion
    Rut
    proveedor=models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE,limit_choices_to={'cargo':'Proveedor'}) """


class venta(ClaseModelo):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, null=True)
    # compras=models.ForeignKey(CarritoProducto,on_delete=models.CASCADE,help_text="Detalle de compras")
    comuna = models.CharField(max_length=40, blank=False, help_text="comuna")
    direccion = models.CharField(max_length=40, blank=False, help_text="direccion")
    precio = models.IntegerField(blank=False)
    estado = models.CharField(max_length=30, null=True, blank=True)
    ciudad = models.CharField(max_length=40, blank=False, null=True)

    # def get_total_stock(self):
    #     return self.cantidad - self.
