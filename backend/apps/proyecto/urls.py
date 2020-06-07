
from django.urls import path, include
from rest_framework import routers
from .views import ProyectoViewset

ROUTER = routers.DefaultRouter()
ROUTER.register("projects", ProyectoViewset)

urlpatterns = [
    # http://localhost:8000/api/projects/<router-viewsets>
    path('', include(ROUTER.urls))
]
