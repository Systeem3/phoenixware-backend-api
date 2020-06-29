from django.urls import path, include
from rest_framework import routers

from .views import RiesgoProyectoViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register("riesgo", RiesgoProyectoViewSet)

urlpatterns = [
    # http://localhost:8000/api/riesgo/<router-viewsets>
    path('', include(ROUTER.urls)),
]
