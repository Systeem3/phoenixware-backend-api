from rest_framework import serializers
from .models import Actividad, Asignacion


class ActividadSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'
        extra_kwargs = {'proceso': {'required': False}}


class AsignacionSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Asignacion
        fields = '__all__'
        extra_kwargs = {'Actividad': {'required': False}}
