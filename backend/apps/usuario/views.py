"""Views of the usuario app"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_auth.registration.views import RegisterView
from django.utils.translation import ugettext_lazy as _
from notifications.signals import notify

from .serializers import UsuarioSerializer
from .models import Usuario
from .permissions import IsAuthenticatedAndAdminUser, AllowAnyUser
from utility.utility import send_mail


class UsuarioListViewSet(ListAPIView):
    """Shows the list users """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAnyUser, ]

    def list(self, request, *args, **kwargs):
        queryset = Usuario.objects.filter(is_active=True)
        serializer = UsuarioSerializer(queryset, many=True)
        return Response(serializer.data)


class UsuarioDetailUpdateViewSet(RetrieveUpdateAPIView):
    """gets an user data and allow update it"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    # permission_classes = [IsAuthenticatedAndAdminUser, ]
    permission_classes = [AllowAnyUser, ]


class CustomRegisterView(RegisterView):
    """adding permission to only admin users"""
    #    permission_classes = [IsAuthenticatedAndAdminUser, ]
    permission_classes = [AllowAnyUser, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Set some values to trigger the send_email function
        values = {
            'subject': 'subject',
            'to_email': request.data.get('email'),
            'html_email_template': 'registration_email.html',
            'context': {
                'nombre': request.data.get('nombre')
            }
        }
        send_mail(**values)
        response = {
            "detail": _("Registro exitoso ")
        }
        notify.send(request.user, recipient=user, verb='Bienvenido a PhoenixWare',
                    description='Bienvenido a PhoenixWare')
        return Response(response,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user
