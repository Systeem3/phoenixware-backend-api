from django.db import models
from ..proyecto.models import Proyecto


# Create your models here.


class Recurso(models.Model):
    TYPE = (
        ("1", "Recursos Humanos"),
        ("2", "Recursos físicos no depreciables"),
        ("3", "Recursos físicos depreciables"),
        ("4", "Recursos intangibles"),
    )
    TYPE_COSTO = (
        ("1", "Costo Directos"),
        ("2", "Costos Indirectos"),
        ("3", "Costo Extraordinarios"),
    )
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=1, choices=TYPE)
    tipo_costo = models.CharField(max_length=1, choices=TYPE_COSTO)
    costo = models.DecimalField(max_digits=10, decimal_places=3)
    estado = models.CharField(max_length=1)

    class Meta:
        db_table = 'Recurso'


class Requisito(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = 'Requisito'


class Objetivo(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = 'Objetivo'


class Seguridad(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = 'Seguridad'


class Artefacto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    enlace = models.URLField()
    estado = models.CharField(max_length=1)

    class Meta:
        db_table = 'Artefacto'
