from rest_framework import permissions
from .models import Miembro


class IsLider(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_authenticated:
            user = request.user
            proyecto = obj.proyecto
            miembro = Miembro.objects.filter(proyecto=proyecto, usuario=user)
            if miembro.rol == "L":
                return True
            return False
        return False
