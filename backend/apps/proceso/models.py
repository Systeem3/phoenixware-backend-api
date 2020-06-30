from django.db import models
from ..proyecto.models import Proyecto


# Create your models here.

class Proceso(models.Model):
    CATEGORIA = (
        ("1", "Inicio"),
        ("2", "Diseño"),
        ("3", "Elaboración"),
        ("4", "ejecución"),
        ("5", "Cierre")
    )
    TIPO = (
        ("G", "Gerencial"),
        ("T", "Tecnico"),
        ("A", "Apoyo")
    )
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    categoria = models.CharField(max_length=1, choices=CATEGORIA)
    tipo = models.CharField(max_length=1, choices=TIPO)
    estado = models.CharField(max_length=1)

    class Meta:
        db_table = 'Proceso'
        unique_together = (('nombre', 'proyecto'),)
