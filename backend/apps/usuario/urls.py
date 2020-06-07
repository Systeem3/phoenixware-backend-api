# from allauth.account.views import confirm_email
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from .views import UsuarioListViewSet, UsuarioDetailUpdateViewSet, CustomRegisterView

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration/', CustomRegisterView.as_view(), name='rest_register'),
    path('token/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('list-users/', UsuarioListViewSet.as_view()),
    path('update-user/<pk>/', UsuarioDetailUpdateViewSet.as_view()),
]
