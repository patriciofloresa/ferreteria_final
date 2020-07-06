from apps.bases.models import ClaseModelo
from apps.producto.models import Carrito, CarritoProducto, Categoria, Producto
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

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
    LISTA_TIPOS_DOCUMENTOS = (
        ('BOLETA', 'Boleta'),
        ('FACTURA', 'Factura'),
    )
    LISTA_TIPOS_DESPACHO = (
        ('DOMICILIO', 'Domicilio'),
        ('TIENDA', 'Recojo en tienda'),
    )
    LISTA_ESTADOS = (
        ('BORRADOR', 'BORRADOR'),
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
    )
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, null=True)
    direccion = models.CharField('Dirección', max_length=250, blank=True, null=True, help_text="direccion")
    ciudad = models.CharField('Ciudad', max_length=100, blank=True, null=True)
    comuna = models.CharField('Comuna', max_length=100, blank=True, null=True, help_text="comuna")
    tipo_documento = models.CharField('Tipo documento', max_length=15, null=True, blank=False, default='BOLETA',
                                      choices=LISTA_TIPOS_DOCUMENTOS)
    tipo_despacho = models.CharField('Estado', max_length=15, null=True, blank=False, default='TIENDA',
                                     choices=LISTA_TIPOS_DESPACHO)
    cli_nombres = models.CharField('Nombres', max_length=250, blank=True, null=True)
    cli_apellidos = models.CharField('Apellidos', max_length=250, blank=True, null=True)
    cli_rut = models.CharField('Rut', max_length=250, blank=True, null=True)
    cli_empresa = models.CharField('Empresa', max_length=250, blank=True, null=True)
    precio = models.IntegerField('Precio', blank=False, default=0)  # costo total de la venta
    estado = models.CharField('Estado', max_length=30, blank=False, default='BORRADOR', choices=LISTA_ESTADOS)

    def __str__(self):
        return "{}".format(self.id)

    def actualiza_stock(self):
        for item in self.carrito.detalles.all():
            item.producto.actualizarStock(item.cantidad*-1)
            item.producto.save()
