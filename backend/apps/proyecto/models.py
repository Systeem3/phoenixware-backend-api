from django.db import models


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


class Miembro(models.Model):
    pass


class Rol(models.Model):
    pass


class RiesgoProyecto(models.Model):
    pass


class Riesgo(models.Model):
    pass


class detalleProyecto(models.Model):
    pass
