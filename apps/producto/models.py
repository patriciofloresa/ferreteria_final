from apps.bases.models import ClaseModelo
from apps.users.models import User

# from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
import json
import requests
 
# Creamos la clase categoria
class Categoria(ClaseModelo):
    Nombre = models.CharField(
        max_length=50, help_text="Nombre de la categoria", unique=True
    )

    def __str__(self):
        return "{}".format(self.Nombre)

    def save(self):
        self.Nombre = self.Nombre.upper()
        super(Categoria, self).save()

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class TipoProducto(ClaseModelo):
    UNIT_CHOICES = (
        ("Kgs", "Kilogramos"),
        ("Lts", "Litros"),
        ("Un", "Unidades"),
    )
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=50, help_text="Nombre de la categoria")
    Um = models.CharField("unidad de medida", max_length=15, choices=UNIT_CHOICES,)

    def __str__(self):
        return "{}:{}".format(self.categoria.Nombre, self.Nombre)

    def save(self):
        self.Nombre = self.Nombre.upper()
        super(TipoProducto, self).save()

    class Meta:
        verbose_name_plural = "Tipos de Productos"
        unique_together = ("categoria", "Nombre")


class Marca(ClaseModelo):
    """
    Marca de un Producto 
    """

    nombre = models.CharField("Nombre", max_length=30, default="Marca")

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nombre


class Producto(ClaseModelo):
    Nombre = models.CharField(max_length=40, blank=False, help_text="Nombre de producto" )
    codigo = models.CharField(primary_key=True, max_length=18)
    precio = models.FloatField(default=0)
    descripcion = models.CharField(max_length=100, help_text="Descripcion de productos", default="descripcion")
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    color = models.CharField(max_length=20, help_text="Color del producto", null=True, blank=True)
    stock = models.IntegerField()
    id_proveedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     limit_choices_to={"cargo": "Proveedor"}, )
    imagen = models.ImageField(upload_to="ferreteria",  null=True, blank=True)
    Categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    TipoProducto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.Nombre)

    def save(self):
        self.Nombre = self.Nombre.upper()
        super(Producto, self).save()

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def actualizarStock(self, cantidad):
        # 10 => compro 5 ==> enviar (-5)
        # x = 10 + (-5) => 5
        if cantidad:
            try:
                self.stock += int(cantidad)
                self.save()
            except Exception as e:
                print("Error : {}".format(str(e)))

    def limit_stock(self):
        item=self.stock
        item=int(item)
        if (item <= 25):
            return 1
        if (item <= 60):
            return 2
        if (item >= 61 ):   
            return 3


class Carrito(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ESTATUS = [
        ("open", "Abierto"),
        ("pagado", "Pagado"),
        ("pendiente", "Pendiente"),
    ]
    estatus = models.CharField(max_length=59, choices=ESTATUS, default="open",)
    monto_total = models.FloatField('Monto total', default=0)

    def get_total(self):
        total = 0
        for carrito_producto in self.detalles.all():
            total += carrito_producto.producto.precio * carrito_producto.cantidad
        return total

    def __str__(self):
        return "{}".format(self.id)


class CarritoProducto(models.Model):
    carrito = models.ForeignKey(
        Carrito, on_delete=models.CASCADE, related_name="detalles"
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)

    def get_precio_parcial(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        return "{}".format(self.id)
