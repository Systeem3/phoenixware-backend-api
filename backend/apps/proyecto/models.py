from django.db import models
from ..usuario.models import Usuario


class Metodologia(models.Model):
    TYPE = (
        ("A", "Agil"),
        ("H", "Hibrido"),
        ("T", "Tradicional")
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=1, choices=TYPE)
    estado = models.CharField(max_length=1)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Metodologia'


class Proyecto(models.Model):
    TYPE_PROJECT = (
        ("S", "Servicio"),
        ("P", "Producto"),
    )
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=1, choices=TYPE_PROJECT)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    alcance = models.TextField(blank=True)
    presupuesto = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    tiempo = models.PositiveSmallIntegerField()
    estado = models.CharField(max_length=1)
    metodologia = models.ForeignKey(Metodologia, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Proyecto'


class Miembro(models.Model):
    ROL = (
        ("M", "Miembro"),
        ("L", "Lider"),
    )
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    # puntuacion = models.DecimalField()
    # estado = models.CharField(max_length=1)
    rol = models.CharField(max_length=1, choices=ROL)

    class Meta:
        db_table = 'Miembro'
        unique_together = (('proyecto', 'usuario'),)


class Reunion(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.CharField(max_length=10)
    lugar = models.CharField(max_length=255)
    estado = models.CharField(max_length=1)

    class Meta:
        db_table = 'Reunion'
