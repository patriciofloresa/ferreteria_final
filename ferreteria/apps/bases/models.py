from django.db import models

# Create your models here.
class ClaseModelo(models.Model):
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
