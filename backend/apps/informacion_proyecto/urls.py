from django.urls import path, include
from rest_framework import routers

from .views import (
    InfoProyectoViewSet,
    RecursoModelViewset,
    RequisitoModelViewset,
    SeguridadModelViewset,
    ObjetivoModelViewset,
    ArtefactoModelViewset
)
ROUTER = routers.DefaultRouter()
ROUTER.register("info_proyecto", InfoProyectoViewSet)
ROUTER.register("requisito", RequisitoModelViewset)
ROUTER.register("recurso", RecursoModelViewset)
ROUTER.register("seguridad", SeguridadModelViewset)
ROUTER.register("objetivo", ObjetivoModelViewset)
ROUTER.register("artefacto", ArtefactoModelViewset)

urlpatterns = [
    # http://localhost:8000/api/riesgo/<router-viewsets>
    path('', include(ROUTER.urls)),
]
