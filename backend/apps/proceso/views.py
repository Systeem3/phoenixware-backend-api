from rest_framework import (
    permissions,
    status,
    viewsets
)
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.translation import ugettext_lazy as _

from .models import Proceso
from .serializers import ProcesoSerilizer
from ..actividad.models import Actividad
from ..actividad.serializers import ActividadSerilizer
from ..proyecto.models import Miembro, Proyecto
from ..proyecto.serializers import MiembroSerializer



# Create your views here.

class ProcesoModelViewSet(viewsets.ModelViewSet):
    queryset = Proceso.objects.all()
    serializer_class = ProcesoSerilizer
    permission_classes = [permissions.IsAuthenticated]
    """lookup_field = 'pk'
    lookup_url_kwarg = 'process_pk'"""

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def crear_actividad(self, request, pk=None):

        my_process = self.get_object()

        user = request.user
        if user.tipo_usuario == "2":
            serializer = ActividadSerilizer(data=request.data)
            if serializer.is_valid():
                serializer.save(proceso=my_process)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        proyecto_pk = request.GET["proyecto_pk"]
        if proyecto_pk is not None:
            my_proyecto = Proyecto.objects.get(pk=proyecto_pk)
            miembro_query = Miembro.objects.filter(proyecto=my_proyecto, usuario=user)
            miembro_serializer = MiembroSerializer(miembro_query, many=True)

            if len(miembro_serializer.data) > 0:
                if miembro_serializer.data[0]["rol"] == "L":
                    serializer = ActividadSerilizer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(proceso=my_process)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if proyecto_pk is None:
            return Response({"detail": _("Debe ingresar el id del proyecto")}, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "detail": _("No permitido")
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def listar_actividades(self, request, pk=None):
        my_procress = self.get_object()
        self.queryset = Actividad.objects.filter(proceso=my_procress)
        serializer = ActividadSerilizer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def listar_actividades_asociadas(self, request, pk=None):
        my_procress = self.get_object()
        user = request.user
        proyecto_pk = request.GET["proyecto_pk"]
        my_proyecto = Proyecto.objects.get(pk=proyecto_pk)
        if proyecto_pk is not None:
            miembro_query = Miembro.objects.filter(proyecto=my_proyecto, usuario=user)
            miembro_serializer = MiembroSerializer(miembro_query, many=True)
            if len(miembro_serializer.data) > 0:
                if miembro_serializer.data[0]["rol"] == "L":
                    self.queryset = Actividad.objects.filter(proceso=my_procress)
                else:
                    query = """select * from Actividad
                                inner join Asignacion on Asignacion.miembro_id={}
                                where Asignacion.actividad_id=Actividad.id""".format(miembro_serializer.data[0]["id"])
                    self.queryset = Actividad.objects.raw(query)
                serializer = ActividadSerilizer(self.queryset, many=True)
                return Response(serializer.data)
            return Response({"detail": _("no es miembro del proyecto")}, status=status.status.HTTP_403_FORBIDDEN)
        return Response({"detail": _("Debe ingresar el id del proyecto")}, status=status.HTTP_400_BAD_REQUEST)
