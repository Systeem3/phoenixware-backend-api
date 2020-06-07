from rest_framework import (
    viewsets,
    permissions
)
from .models import Proyecto
from .serializers import ProyectoSerializer


class ProyectoViewset(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [permissions.AllowAny, ]
