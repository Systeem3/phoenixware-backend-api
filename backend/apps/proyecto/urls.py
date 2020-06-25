from django.urls import path, include
from rest_framework import routers
from .views import ProyectoModelViewset

ROUTER = routers.DefaultRouter()
ROUTER.register("projects", ProyectoModelViewset)

urlpatterns = [
    # http://localhost:8000/api/projects/<router-viewsets>
    path('', include(ROUTER.urls)),
]
