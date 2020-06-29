from rest_framework import (
    permissions,
    status,
    viewsets
)
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.translation import ugettext_lazy as _

from .models import Riesgo, RiesgoProyecto
from .serializers import RiesgoSerilizer, RiesgoProyectoSerilizer
from ..proyecto.models import Miembro, Proyecto
from ..proyecto.serializers import MiembroSerializer, ProyectoSerializer


# Create your views here.


class RiesgoProyectoViewSet(viewsets.GenericViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = RiesgoSerilizer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def crear_riesgo_proyecto(self, request, pk=None):
        my_project = self.get_object()
        user = request.user
        if user.tipo_usuario == "2":
            serializer = RiesgoProyectoSerilizer(data=request.data)
            if serializer.is_valid():
                serializer.save(proyecto=my_project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        miembro_query = Miembro.objects.filter(proyecto=my_project, usuario=user)
        miembro_serializer = MiembroSerializer(miembro_query, many=True)

        if len(miembro_serializer.data) > 0:
            if miembro_serializer.data[0]["rol"] == "L":
                serializer = RiesgoProyectoSerilizer(data=request.data)
                if serializer.is_valid():
                    serializer.save(proyecto=my_project)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "detail": _("No permitido")
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def listar_riesgos_proyecto(self, request, pk=None):
        my_project = self.get_object()
        self.queryset = RiesgoProyecto.objects.filter(proyecto=my_project)
        serializer = RiesgoProyectoSerilizer(self.queryset, many=True)
        return Response(serializer.data)


