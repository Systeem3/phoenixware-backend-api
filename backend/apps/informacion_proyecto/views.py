from rest_framework import (
    permissions,
    status,
    viewsets
)
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.translation import ugettext_lazy as _

from .models import (
    Objetivo,
    Requisito,
    Artefacto,
    Seguridad,
    Recurso
)
from .serializers import (
    RecursoSerializer,
    SeguridadSerializer,
    ArtefactoSerializer,
    ObjetivoSerializer,
    RequisitoSerializer
)

from ..proyecto.models import Miembro, Proyecto
from ..proyecto.serializers import MiembroSerializer
from ..actividad.models import Actividad
from ..proceso.models import Proceso
from ..usuario.models import Usuario, Empleado
from utility.utility import (
    get_resources
)


class InfoProyectoViewSet(viewsets.GenericViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = RecursoSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def crear_recurso(self, request, pk=None):
        my_project = self.get_object()
        user = request.user
        if user.tipo_usuario == "2":
            serializer = RecursoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(proyecto=my_project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        miembro_query = Miembro.objects.filter(proyecto=my_project, usuario=user)
        miembro_serializer = MiembroSerializer(miembro_query, many=True)

        if len(miembro_serializer.data) > 0:
            if miembro_serializer.data[0]["rol"] == "L":
                serializer = RecursoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(proyecto=my_project)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "detail": _("No permitido")
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def listar_recursos_proyecto(self, request, pk=None):
        my_project = self.get_object()
        self.queryset = Recurso.objects.filter(proyecto=my_project)
        serializer = RecursoSerializer(self.queryset, many=True)
        response = get_resources(serializer.data)
        return Response(response)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def crear_requisito(self, request, pk=None):
        my_project = self.get_object()
        user = request.user
        if user.tipo_usuario == "2":
            serializer = RequisitoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(proyecto=my_project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        miembro_query = Miembro.objects.filter(proyecto=my_project, usuario=user)
        miembro_serializer = MiembroSerializer(miembro_query, many=True)

        if len(miembro_serializer.data) > 0:
            if miembro_serializer.data[0]["rol"] == "L":
                serializer = RequisitoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(proyecto=my_project)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "detail": _("No permitido")
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def listar_requisitos_proyecto(self, request, pk=None):
        my_project = self.get_object()
        self.queryset = Requisito.objects.filter(proyecto=my_project)
        serializer = RequisitoSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def crear_artefacto(self, request, pk=None):
        my_project = self.get_object()
        user = request.user
        if user.tipo_usuario == "2":
            serializer = ArtefactoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(proyecto=my_project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        miembro_query = Miembro.objects.filter(proyecto=my_project, usuario=user)
        miembro_serializer = MiembroSerializer(miembro_query, many=True)

        if len(miembro_serializer.data) > 0:
            if miembro_serializer.data[0]["rol"] == "L":
                serializer = ArtefactoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(proyecto=my_project)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "detail": _("No permitido")
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def listar_artefacto_proyecto(self, request, pk=None):
        my_project = self.get_object()
        self.queryset = Artefacto.objects.filter(proyecto=my_project)
        serializer = ArtefactoSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def crear_objetivo(self, request, pk=None):
        my_project = self.get_object()
        user = request.user
        if user.tipo_usuario == "2":
            serializer = ObjetivoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(proyecto=my_project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        miembro_query = Miembro.objects.filter(proyecto=my_project, usuario=user)
        miembro_serializer = MiembroSerializer(miembro_query, many=True)

        if len(miembro_serializer.data) > 0:
            if miembro_serializer.data[0]["rol"] == "L":
                serializer = ObjetivoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(proyecto=my_project)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "detail": _("No permitido")
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def listar_objetivo_proyecto(self, request, pk=None):
        my_project = self.get_object()
        self.queryset = Objetivo.objects.filter(proyecto=my_project)
        serializer = ObjetivoSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def crear_seguridad(self, request, pk=None):
        my_project = self.get_object()
        user = request.user
        if user.tipo_usuario == "2":
            serializer = SeguridadSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(proyecto=my_project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        miembro_query = Miembro.objects.filter(proyecto=my_project, usuario=user)
        miembro_serializer = MiembroSerializer(miembro_query, many=True)

        if len(miembro_serializer.data) > 0:
            if miembro_serializer.data[0]["rol"] == "L":
                serializer = SeguridadSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(proyecto=my_project)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "detail": _("No permitido")
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def listar_seguridad_proyecto(self, request, pk=None):
        my_project = self.get_object()
        self.queryset = Seguridad.objects.filter(proyecto=my_project)
        serializer = SeguridadSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def info_proyecto(self, request, pk=None):
        my_project = self.get_object()
        query = """select * from Actividad
                    inner join Proceso on Proceso.proyecto_id={}
                    where Actividad.proceso_id=Proceso.id""".format(my_project.id)
        query2 = """select * from Actividad
                            inner join Proceso on Proceso.proyecto_id={}
                            where Actividad.proceso_id=Proceso.id and Actividad.estado='A'""".format(my_project.id)
        actividades_totales = len(Actividad.objects.raw(query))
        actividades_completadas = len(Actividad.objects.raw(query2))
        miembros_totales = len(Miembro.objects.filter(proyecto=my_project))
        lider = Miembro.objects.filter(proyecto=my_project, rol='L')
        procesos_totales = len(Proceso.objects.filter(proyecto=my_project))
        lider = Usuario.objects.get(pk=lider[0].usuario_id)
        lider = Empleado.objects.get(pk=lider.empleado_id)
        METODOLOGIA = {
            "1": "Agil",
            "2": "Hibrido",
            "3": "Tradicional",
        }
        response = {
            "nombre": my_project.nombre,
            "presupuesto": my_project.presupuesto,
            "costo": my_project.costo,
            "miembros": miembros_totales,
            "actividades_asignadas": actividades_totales,
            "actividades_completadas": actividades_completadas,
            "procesos_totales": procesos_totales,
            "metodologia": METODOLOGIA[my_project.metodologia],
            "fecha_inicio": my_project.fecha_inicio,
            "fecha_finalizacion": my_project.fecha_finalizacion,
            "lider": lider.nombre + " " + lider.apellido
        }
        return Response(response)


class RecursoModelViewset(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer
    permission_classes = [permissions.AllowAny, ]


class RequisitoModelViewset(viewsets.ModelViewSet):
    queryset = Requisito.objects.all()
    serializer_class = RequisitoSerializer
    permission_classes = [permissions.AllowAny, ]


class ObjetivoModelViewset(viewsets.ModelViewSet):
    queryset = Objetivo.objects.all()
    serializer_class = ObjetivoSerializer
    permission_classes = [permissions.AllowAny, ]


class ArtefactoModelViewset(viewsets.ModelViewSet):
    queryset = Artefacto.objects.all()
    serializer_class = ArtefactoSerializer
    permission_classes = [permissions.AllowAny, ]


class SeguridadModelViewset(viewsets.ModelViewSet):
    queryset = Seguridad.objects.all()
    serializer_class = SeguridadSerializer
    permission_classes = [permissions.AllowAny, ]
