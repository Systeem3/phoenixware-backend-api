from rest_framework import serializers
from .models import RiesgoProyecto, Riesgo


class RiesgoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Riesgo
        fields = '__all__'


class RiesgoProyectoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = RiesgoProyecto
        fields = '__all__'
        extra_kwargs = {'proyecto': {'required': False}}
