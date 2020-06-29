from django.db import models
from ..proyecto.models import Proyecto


# Create your models here.


class Riesgo(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255)
    estado = models.CharField(max_length=1)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Riesgo'


class RiesgoProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    riesgo = models.ForeignKey(Riesgo, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True)
    prioridad = models.CharField(max_length=1)
    plan_mitigacion = models.TextField(blank=True)
    plan_contingencia = models.TextField(blank=True)
    evolucion = models.TextField(blank=True)
    probabilidad_ocurrencia = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    magnitud_riesgo = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    estimacion_riesgo = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    comentario = models.TextField(blank=True)
    estado = models.CharField(max_length=1)

    class Meta:
        db_table = 'RisgoProyecto'
        unique_together = (('proyecto', 'riesgo'),)
