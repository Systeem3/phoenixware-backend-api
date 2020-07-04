from django.urls import path, include
from rest_framework import routers

from .views import ActividadModelViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register("actividad", ActividadModelViewSet)
urlpatterns = [
    # http://localhost:8000/api/actividad/<router-viewsets>
    path('', include(ROUTER.urls)),
]
