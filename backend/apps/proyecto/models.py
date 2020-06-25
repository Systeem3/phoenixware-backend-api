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
    descripcion = models.TextField()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha = models.DateField()
    lugar = models.CharField(max_length=255)
    estado = models.CharField(max_length=1)

    class Meta:
        db_table = 'Reunion'



"""class RiesgoProyecto(models.Model):
    pass


class Riesgo(models.Model):
    pass


class detalleProyecto(models.Model):
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)
    # tiempo = models.DateField()
    costo = models.DecimalField()
    presupuesto = models.DecimalField()
    moneda = models.CharField(max_length=1)"""
