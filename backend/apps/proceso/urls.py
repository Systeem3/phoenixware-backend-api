from django.urls import path, include
from rest_framework import routers
from .views import ProcesoModelViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register("process", ProcesoModelViewSet)

urlpatterns = [
    # http://localhost:8000/api/process/<router-viewsets>
    path('', include(ROUTER.urls)),
    path('process/<pk>/crear_actividad/?<int:proyecto_pk>/', ProcesoModelViewSet.as_view({'post', 'crear_actividad'}))
]
