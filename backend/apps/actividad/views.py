from rest_framework import (
    permissions,
    status,
    viewsets
)
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.translation import ugettext_lazy as _
from .models import Actividad, Asignacion
from .serializers import AsignacionSerilizer, ActividadSerilizer
from ..proyecto.models import Proyecto, Miembro
from ..proyecto.serializers import MiembroSerializer
from ..usuario.models import Usuario
from notifications.signals import notify

# Create your views here.


class ActividadModelViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerilizer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def crear_asignacion(self, request, pk=None):
        my_activida = self.get_object()

        user = request.user
        serializer = AsignacionSerilizer(data=request.data)
        if user.tipo_usuario == "2":
            if serializer.is_valid():
                serializer.save(actividad=my_activida)
                pk_miembro = request.data["miembro"]
                usuario = Usuario.objects.get(pk=pk_miembro)
                notify.send(user, recipient=usuario, verb=my_activida.nombre,
                            description=my_activida.descripcion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        proyecto_pk = request.GET["proyecto_pk"]
        if proyecto_pk is not None:
            my_proyecto = Proyecto.objects.get(pk=proyecto_pk)
            miembro_query = Miembro.objects.filter(proyecto=my_proyecto, usuario=user)
            miembro_serializer = MiembroSerializer(miembro_query, many=True)

            if len(miembro_serializer.data) > 0:
                if miembro_serializer.data[0]["rol"] == "L":
                    if serializer.is_valid():
                        serializer.save(actividad=my_activida)
                        pk_miembro = request.data["miembro"]
                        usuario = Usuario.objects.get(pk=pk_miembro)
                        notify.send(user, recipient=usuario, verb=my_activida.nombre,
                                    description=my_activida.descripcion)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if proyecto_pk is None:
            return Response({"detail": _("Debe ingresar el id del proyecto")}, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "detail": _("No permitido")
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def listar_asignacion(self, request, pk=None):
        my_activida = self.get_object()
        self.queryset = Asignacion.objects.filter(actividad=my_activida)
        serializer = AsignacionSerilizer(self.queryset, many=True)
        return Response(serializer.data)

