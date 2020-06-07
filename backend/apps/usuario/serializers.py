# pylint: skip-file
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.utils.translation import ugettext_lazy as _
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from .models import Empleado, Usuario, TipoUsuario


class CustomRegisterSerializer(RegisterSerializer):
    """Custom register serializer"""
    user_types = (
        (1, "administrador"),
        (2, "director"),
        (3, "miembro")
    )
    username = None
    email = serializers.EmailField(required=True)
    password1 = None
    password2 = None

    nombre = serializers.CharField(required=True, write_only=True)
    apellido = serializers.CharField(required=True, write_only=True)
    direccion = serializers.CharField(required=True, write_only=True)
    telefono = serializers.CharField(required=True, write_only=True)
    tipo_usuario = serializers.ChoiceField(required=True, choices=user_types, initial=user_types[0])
    foto = serializers.ImageField(required=False, write_only=True, default='pictures/default.jpg')

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        return data

    def get_cleaned_data(self):
        name = str(self.validated_data.get('nombre', ''))
        last_name = str(self.validated_data.get('apellido', ''))
        password = Usuario.objects.generate_password(name, last_name)

        return {
            'password1': password,
            'email': self.validated_data.get('email', ''),
            'nombre': self.validated_data.get('nombre', ''),
            'apellido': self.validated_data.get('apellido', ''),
            'direccion': self.validated_data.get('direccion', ''),
            'telefono': self.validated_data.get('telefono', ''),
            'tipo_usuario': self.validated_data.get('tipo_usuario', ''),
            'foto': self.validated_data.get('foto', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        empleado = Empleado(
            nombre=self.cleaned_data["nombre"],
            apellido=self.cleaned_data["apellido"],
            direccion=self.cleaned_data["direccion"],
            telefono=self.cleaned_data["telefono"],
            foto=self.cleaned_data["foto"]
        )
        empleado.save()
        tipo_usuario_id = self.cleaned_data["tipo_usuario"]
        user.empleado = empleado
        user.tipo_usuario_id = tipo_usuario_id
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        self.custom_signup(request, user)
        return user


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)
        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'email_template_name': 'password_reset_email.html',
            'request': request,
        }
        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class EmpleadoSerializer(serializers.ModelSerializer):
    """Empleado serilizer"""

    class Meta:
        model = Empleado
        fields = ('nombre', 'apellido', 'direccion', 'telefono', 'foto')


class TipoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUsuario
        fields = ('id', 'nombre',)
        read_only_fields = ('id', 'nombre',)


class UsuarioSerializerAuthenticated(serializers.ModelSerializer):
    """shows the details from the authenticated user"""
    empleado = EmpleadoSerializer()
    tipo_usuario = TipoUsuarioSerializer(required=False)

    class Meta:  # pylint: disable=too-few-public-methods
        model = Usuario
        fields = ('email', 'empleado', 'tipo_usuario')

    def update(self, instance, validated_data):
        """overwrited update method for handle nested representations"""
        empleado_data = validated_data.pop('empleado')

        empleado = instance.empleado

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        empleado.nombre = empleado_data.get('nombre', empleado.nombre)
        empleado.apellido = empleado_data.get('apellido', empleado.apellido)
        empleado.direccion = empleado_data.get('direccion', empleado.direccion)
        empleado.telefono = empleado_data.get('telefono', empleado.telefono)
        empleado.foto = empleado_data.get('foto', empleado.foto)
        empleado.save()

        return instance


class UsuarioSerializer(serializers.ModelSerializer):
    user_types = (
        (1, "administrador"),
        (2, "director"),
        (3, "miembro")
    )
    empleado = EmpleadoSerializer()
    tipo_usuario_write = serializers.ChoiceField(choices=user_types, write_only=True)
    tipo_usuario = TipoUsuarioSerializer(required=False)

    class Meta:
        model = Usuario
        fields = ('id', 'email', 'is_active', 'empleado', 'tipo_usuario_write', 'tipo_usuario')

    def update(self, instance, validated_data):
        """overwrited update method for handle nested representations"""
        empleado_data = validated_data.pop('empleado')
        empleado = instance.empleado

        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.tipo_usuario_id = validated_data.get('tipo_usuario_write', instance.tipo_usuario_id)
        instance.save()

        empleado.nombre = empleado_data.get('nombre', empleado.nombre)
        empleado.apellido = empleado_data.get('apellido', empleado.apellido)
        empleado.direccion = empleado_data.get('direccion', empleado.direccion)
        empleado.telefono = empleado_data.get('telefono', empleado.telefono)
        empleado.foto = empleado_data.get('foto', empleado.foto)
        empleado.save()

        return instance

