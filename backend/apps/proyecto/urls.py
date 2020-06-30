from django.urls import path, include
from rest_framework import routers
from .views import ProyectoModelViewset, ReunionModelViewset, DeleteMiembro

ROUTER = routers.DefaultRouter()
ROUTER.register("projects", ProyectoModelViewset)
ROUTER.register("reunion", ReunionModelViewset)
urlpatterns = [
    # http://localhost:8000/api/projects/<router-viewsets>
    path('', include(ROUTER.urls)),
    path('miembro/<pk>/delete/', DeleteMiembro.as_view())
]
