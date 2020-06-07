"""Views of the usuario app"""
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_auth.registration.views import RegisterView

from .serializers import UsuarioSerializer
from .models import Usuario
from .permissions import IsAuthenticatedAndAdminUser


class UsuarioListViewSet(ListAPIView):
    """Shows the list users """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticatedAndAdminUser, ]


class UsuarioDetailUpdateViewSet(RetrieveUpdateAPIView):
    """gets an user data and allow update it"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticatedAndAdminUser, ]


class CustomRegisterView(RegisterView):
    """adding permission to only admin users"""
    permission_classes = [IsAuthenticatedAndAdminUser, ]
