from django.db import models
from datetime import datetime

# Create your models here.
class ClaseModelo(models.Model):
    fc = models.DateTimeField(default=datetime.now)
    fm = models.DateTimeField(default=datetime.now)

    class Meta:
        abstract = True
