from django.db import models
from ferreteria.settings import MEDIA_URL, STATIC_URL
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    cargo_choices = (
        ("cliente","cliente"),
        ("proveedor","proveedor"),
        ("empleados","empleados"),
        ("ventas","ventas")
    )
    # staff_choices = (
    #     ("1","Si"),
    #     ("0","No")
    # )
    # is_staff = models.IntegerField(max_length=254, null=True, blank=True,choices=staff_choices, default=0)
    # is_superuser  = models.IntegerField(max_length=254, null=True, blank=True,choices=staff_choices, default=0)
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    rut = models.CharField(unique=True,null=True,blank=True, max_length=10)
    cargo = models.CharField(max_length=254, null=True, blank=True,choices=cargo_choices, default="cliente")
    celular = models.IntegerField(unique=True,null=True,blank=True)

    def get_absolute_url(self):
	    return "/users/%i/" % (self.pk)

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

