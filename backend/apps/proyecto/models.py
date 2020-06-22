from django.db import models
from ..usuario.models import Usuario


class Proyecto(models.Model):
    TYPE_PROJECT = (
        ("A", "Agil"),
        ("H", "Hibrido"),
        ("T", "Tradicional")
    )
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=1, choices=TYPE_PROJECT)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    estado = models.CharField(max_length=1)

    class Meta:
        db_table = 'Proyecto'


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


class Rol(models.Model):
    metodologia = models.ForeignKey(Metodologia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255)
    descripcion = models.TextField()
    estado = models.CharField(max_length=1)

    class Meta:
        db_table = 'Rol'


class Miembro(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    puntuacion = models.DecimalField()
    estado = models.CharField(max_length=1)

    class Meta:
        db_table = 'Miembro'


class RiesgoProyecto(models.Model):
    pass


class Riesgo(models.Model):
    pass


class detalleProyecto(models.Model):
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)
    # tiempo = models.DateField()
    costo = models.DecimalField()
    presupuesto = models.DecimalField()
    moneda = models.CharField(max_length=1)
