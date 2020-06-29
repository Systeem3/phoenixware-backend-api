from django.db import models
from ..proyecto.models import Proyecto
# Create your models here.


class Recurso(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    tipo_recurso = models.CharField(max_length=1)
    tipo_costo = models.CharField(max_length=1)
    costo = models.DecimalField(max_digits=10, decimal_places=3)
    estado = models.CharField(max_length=1)


class Requisito(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)


class Objetivo(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)


class Seguridad(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)