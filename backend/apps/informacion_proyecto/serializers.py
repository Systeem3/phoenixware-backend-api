from rest_framework import serializers
from .models import (
    Artefacto,
    Requisito,
    Objetivo,
    Recurso,
    Seguridad
)


class ArtefactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artefacto
        fields = '__all__'
        extra_kwargs = {'proyecto': {'required': False}}


class RequisitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisito
        fields = '__all__'
        extra_kwargs = {'proyecto': {'required': False}}


class ObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objetivo
        fields = '__all__'
        extra_kwargs = {'proyecto': {'required': False}}


class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = '__all__'
        extra_kwargs = {'proyecto': {'required': False}}


class SeguridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguridad
        fields = '__all__'
        extra_kwargs = {'proyecto': {'required': False}}
