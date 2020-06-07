"""  Modelos Usuario, tipo de usuario y empleado"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


# Create your models here.
class Empleado(models.Model):
    """Modelo empleado"""
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    foto = models.ImageField(
        upload_to='pictures/%y/%m/%d',
        default='pictures/default.jpg',
        max_length=255
    )
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:  # pylint: disable=too-few-public-methods
        """Propiedades adicionales del modelo Empleado"""
        db_table = 'Empleado'


class TipoUsuario(models.Model):
    """Modelo Tipo de usuario"""
    nombre = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:  # pylint: disable=too-few-public-methods
        """Propiedades adicionales del modelo TipoUsuario"""
        db_table = 'TipoUsuario'


class Usuario(AbstractUser):
    """ Modelo Usuario """
    username = None
    email = models.EmailField(_('Correo electronico'), unique=True)
    USERNAME_FIELD = 'email'
    first_name = None
    last_name = None
    is_staff = None
    is_superuser = None
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    REQUIRED_FIELDS = ['empleado', 'tipo_usuario']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:  # pylint: disable=too-few-public-methods
        """Propiedades adicioneles del modelo Usuario"""
        db_table = 'Usuario'

