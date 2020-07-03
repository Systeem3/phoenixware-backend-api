from rest_framework import (
    viewsets,
    permissions,
    status
)
from rest_framework.generics import (
    DestroyAPIView
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from notifications.signals import notify

from .models import Proyecto, Reunion, Miembro
from .serializers import ProyectoSerializer, ReunionSerializer, MiembroSerializer
from ..usuario.models import Usuario
from ..usuario.serializers import UsuarioSerializer
from ..proceso.serializers import ProcesoSerilizer
from ..proceso.models import Proceso
from utility.utility import (
    get_list_users,
    get_miembros,
    get_time,
    get_proyectos,
    get_procesos
)


class ProyectoModelViewset(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [permissions.AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = ProyectoSerializer(data=request.data)
        if serializer.is_valid():
            tiempo = get_time(request.data["fecha_inicio"], request.data["fecha_finalizacion"])
            serializer.save(tiempo=tiempo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        self.permission_classes = [permissions.IsAuthenticated, ]
        user = request.user
        if user.tipo_usuario == "1" or user.tipo_usuario == "2":
            self.queryset = Proyecto.objects.filter(estado='A')
        else:
            query = """select * from Proyecto 
                        inner join miembro on miembro.proyecto_id=Proyecto.id 
                        where miembro.usuario_id={} and Proyecto.estado='A'""".format(user.id)
            self.queryset = Proyecto.objects.raw(query)
        serializer = ProyectoSerializer(self.queryset, many=True)
        response = get_proyectos(serializer.data)

        return Response(response)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def crear_reunion(self, request, pk=None):
        my_proyecto = self.get_object()
        user = request.user
        miembro_query = Miembro.objects.filter(proyecto=my_proyecto, usuario=user)
        miembro_serializer = MiembroSerializer(miembro_query, many=True)
        if len(miembro_serializer.data) > 0:
            if miembro_serializer.data[0]["rol"] == "L":
                serializer = ReunionSerializer(data=request.data)
                if serializer.is_valid():
                    reunion = serializer.save(proyecto=my_proyecto)
                    query = """select * from Usuario
                                inner join miembro on miembro.proyecto_id={}
                                where miembro.usuario_id=Usuario.id""".format(my_proyecto.id)
                    queryset = Usuario.objects.raw(query)
                    usuario_serializer = UsuarioSerializer(queryset, many=True)
                    list_users = get_list_users(usuario_serializer.data)
                    notify.send(user, recipient=list_users, verb=reunion.nombre,
                                description=reunion.descripcion)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "detail": _("No permitido")
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'])
    def listar_reuniones(self, request, pk=None):
        my_proyecto = self.get_object()
        self.queryset = Reunion.objects.filter(proyecto=my_proyecto)
        serializer = ReunionSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def agregar_miembro(self, request, pk=None):
        user = request.user
        if user.tipo_usuario == "2":
            my_proyecto = self.get_object()
            serializer = MiembroSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(proyecto=my_proyecto)
                usuario = Usuario.objects.get(pk=request.data["usuario"])
                notify.send(request.user, recipient=usuario, verb="te agregaron a un proyecto",
                            description="bienvenido al proyecto")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "detail": _("No permitido")
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'])
    def listar_miembros(self, request, pk=None):
        my_proyecto = self.get_object()
        self.queryset = Miembro.objects.filter(proyecto=my_proyecto)
        serializer = MiembroSerializer(self.queryset, many=True)
        response = get_miembros(serializer.data)
        return Response(response)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def usuarios_no_pertenecen(self, request, pk=None):
        my_proyecto = self.get_object()
        query = """select * from Usuario WHERE Usuario.id NOT IN 
                    (select Miembro.usuario_id from Miembro where Miembro.proyecto_id={});""".format(my_proyecto.id)
        self.queryset = Usuario.objects.raw(query)
        serializer = UsuarioSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def crear_proceso(self, request, pk=None):
        my_proyecto = self.get_object()
        user = request.user
        if user.tipo_usuario == "2":
            serializer = ProcesoSerilizer(data=request.data)
            if serializer.is_valid():
                serializer.save(proyecto=my_proyecto)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        miembro_query = Miembro.objects.filter(proyecto=my_proyecto, usuario=user)
        miembro_serializer = MiembroSerializer(miembro_query, many=True)

        if len(miembro_serializer.data) > 0:
            if miembro_serializer.data[0]["rol"] == "L":
                serializer = ProcesoSerilizer(data=request.data)
                if serializer.is_valid():
                    serializer.save(proyecto=my_proyecto)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "detail": _("No permitido")
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def listar_procesos(self, request, pk=None):
        my_proyecto = self.get_object()
        self.queryset = Proceso.objects.filter(proyecto=my_proyecto)
        serializer = ProcesoSerilizer(self.queryset, many=True)
        response = get_procesos(serializer.data)
        return Response(response)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def listar_procesos_categoria(self, request, pk=None):
        my_proyecto = self.get_object()
        categoria = request.GET["categoria"]
        self.queryset = Proceso.objects.filter(proyecto=my_proyecto, categoria=categoria)
        serializer = ProcesoSerilizer(self.queryset, many=True)
        return Response(serializer.data)


class ReunionModelViewset(viewsets.ModelViewSet):
    queryset = Reunion.objects.all()
    serializer_class = ReunionSerializer
    permission_classes = [permissions.AllowAny, ]


class DeleteMiembro(DestroyAPIView):
    queryset = Miembro.objects.all()
    serializer_class = MiembroSerializer
    permission_classes = [permissions.AllowAny, ]
