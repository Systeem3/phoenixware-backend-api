from django.db import models
from ..proceso.models import Proceso
from ..proyecto.models import Miembro


# Create your models here.

class Actividad(models.Model):
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    # predecesor = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    estado = models.CharField(max_length=1)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Actividad'


class Asignacion(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    puntuacion = models.DecimalField(max_digits=5, decimal_places=3, null=True)

    class Meta:
        db_table = 'Asignacion'
        unique_together = (('miembro', 'actividad'),)
