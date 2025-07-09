from rest_framework import serializers
from Api.models.user_model import User
from Api.models.permission_model import CustomPermission

class AssignPermissionSerializer(serializers.Serializer):
    permissions = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )

    def validate_permissions(self, value):
        not_found = []
        for pid in value:
            if not CustomPermission.objects.filter(id=pid).exists():
                not_found.append(pid)
        if not_found:
            raise serializers.ValidationError(f"Permisos no encontrados: {not_found}")
        return value

    def save(self, user):
        permisos = CustomPermission.objects.filter(id__in=self.validated_data['permissions'])
        user.permissions.add(*permisos)
        return user
