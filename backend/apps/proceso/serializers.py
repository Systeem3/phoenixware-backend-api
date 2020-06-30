from rest_framework import serializers
from .models import Proceso


class ProcesoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Proceso
        fields = '__all__'
        extra_kwargs = {'proyecto': {'required': False}}
