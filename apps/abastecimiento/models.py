from django.db import models
from django.forms import model_to_dict

from apps.producto.models import Producto
from apps.users.models import User


class Pedido(models.Model):
    LISTA_DOCUMENTOS = (
        ('BOLETA', 'Boleta'),
        ('FACTURA', 'Factura'),
    )
    LISTA_TIPOS_PAGO = (
        ('CONTADO', 'Contado'),
        ('CREDITO', 'Credito'),
    )
    LISTA_ESTADOS = (
        ('BORRADOR', 'BORRADOR'),
        ('PENDIENTE', 'Pendiente'),
        ('ACEPTADO', 'Aceptado'),
        ('ENVIADO', 'Enviado'),
        ('RECIBIDO', 'Recibido'),
    )
    numero = models.CharField('Número', max_length=45)
    fecha = models.DateField('Fecha')
    tipo_documento = models.CharField('Tipo documento', max_length=15, blank=False, default='BOLETA',
                                      choices=LISTA_DOCUMENTOS)
    tipo_pago = models.CharField('Tipo pago', max_length=15, blank=False, default='CONTADO',
                                 choices=LISTA_TIPOS_PAGO)
    total = models.FloatField('Total', default=0)
    estado = models.CharField('Estado', max_length=15, blank=False, default='BORRADOR',
                              choices=LISTA_ESTADOS)
    proveedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos_proveedor')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos_usuario')

    def __str__(self):
        return "{}".format(self.pk)

    class Meta:
        permissions = (
            ('access_modulo_abastecimiento', '* Access modulo abastecimiento'),
            ('list_pedido', 'List pedido'),
        )

    def toJSON(self):
        # muestra todos los campos del modelo con excepcion de los exclude
        item = model_to_dict(self, exclude=[])
        item['fecha'] = self.fecha.strftime("%d/%m/%Y")
        item['proveedor_name'] = self.proveedor.get_full_name()
        item['usuario_name'] = self.usuario.username
        return item

    def confirmar_pedido(self):
        self.estado = "PENDIENTE"

    def aceptar_pedido(self):
        self.estado = "ACEPTADO"

    def enviar_pedido(self):
        self.estado = "ENVIADO"

    def recibir_pedido(self):
        self.estado = "RECIBIDO"

    def actualiza_stock(self):
        for item in self.detalles.all():
            item.producto.actualizarStock(item.cantidad)
            item.producto.save()


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles_pedido')
    precio = models.FloatField('precio', default=0)
    cantidad = models.FloatField('cantidad', default=0)
    total = models.FloatField('total', default=0)

    def __str__(self):
        return "{}".format(self.pk)
