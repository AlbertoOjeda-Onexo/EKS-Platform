from django.db import models
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class CustomPermission(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code    

class HasCustomPermission(BasePermission):
    def has_permission(self, request, view):
        required_permission = getattr(view, 'required_permission', None)
        if required_permission is None:
            return True  

        user = request.user
        if not user or not user.is_authenticated:
            return False

        if not user.permissions.filter(code=required_permission).exists():
            raise PermissionDenied({
                "code": "Permiso denegado",
                "detail": "No cuenta con autorización para realizar esta acción"
            })

        return True