"""Permissions"""
from rest_framework import permissions


class IsAuthenticatedAndAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = request.user
            return user.tipo_usuario == "1"
        return False


class AllowAnyUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return permissions.AllowAny
