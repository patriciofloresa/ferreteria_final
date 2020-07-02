from django.contrib.auth.models import AbstractUser
from django.db import models
from ferreteria.settings import MEDIA_URL, STATIC_URL


class User(AbstractUser):
    LISTA_CARGOS = (
        ('Proveedor', 'Proveedor'),
        ('Cliente', 'Cliente'),
        ('Empleado', 'Empleado'),
        ('Administrador', 'Administrador'),
        ('Venta', 'Venta'),
    )
    image = models.ImageField(upload_to="users/%Y/%m/%d", null=True, blank=True)
    rut = models.CharField(max_length=254, null=True, blank=True, unique=True)
    cargo = models.CharField(max_length=254, null=True, blank=True, default="Cliente", choices=LISTA_CARGOS)
    celular = models.IntegerField(unique=True, null=True, blank=True)
    username = models.CharField(unique=False, default='', max_length=100)

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def get_image(self):
        if self.image:
            return "{}{}".format(MEDIA_URL, self.image)
        return "{}{}".format(STATIC_URL, "img/empty.png")

    def __str__(self):
        return "{}".format(self.username)
