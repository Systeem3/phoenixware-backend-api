"""Serilizers proyecto apps"""
from rest_framework import serializers
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

from .models import Proyecto, Reunion, Miembro


class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'
        extra_kwargs = {'tiempo': {'required': False}}

"""    def validate_fecha_inicio(self, fecha_inicio):
        if fecha_inicio < datetime.now().date():
            raise serializers.ValidationError(_("Date cannot be in the past"))
        return fecha_inicio

    def validate(self, data):
        if data["fecha_finalizacion"] < data["fecha_inicio"]:
            raise serializers.ValidationError(_("la fecha de finalizacion no puede ser menor a la de inicio"))
        return data"""


class ReunionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reunion
        fields = '__all__'
        extra_kwargs = {'proyecto': {'required': False},
                        'descripcion': {'required': False}}

    def validate_fecha(self, fecha):
        if fecha < datetime.now().date():
            raise serializers.ValidationError(_("Date cannot be in the past"))
        return fecha


class MiembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Miembro
        fields = '__all__'
        extra_kwargs = {'proyecto': {'required': False}}
