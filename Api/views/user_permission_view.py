from rest_framework import status
from Api.models.user_model import User
from rest_framework.views import APIView
from rest_framework.response import Response
from Api.models.permission_model import CustomPermission
from Api.serializers.user_permission_serializer import AssignPermissionSerializer

class UserPermissionView(APIView):
    def get(self, request, idUser):
        user = User.objects.filter(idUser=idUser).first()
        if not user:
            return Response({"detail": "Usuario no encontrado"}, status=404)

        permisos = user.permissions.all().values("id", "code", "description")
        return Response(permisos, status=200)

    def post(self, request, idUser):
        user = User.objects.filter(idUser=idUser).first()
        if not user:
            return Response({"detail": "Usuario no encontrado"}, status=404)

        serializer = AssignPermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user)
            return Response({"message": "Permisos asignados correctamente"}, status=200)
        return Response(serializer.errors, status=400)

class UserPermissionRemoveView(APIView):
    def delete(self, request, idUser, permiso_id):
        user = User.objects.filter(idUser=idUser).first()
        if not user:
            return Response({"detail": "Usuario no encontrado"}, status=404)

        permiso = CustomPermission.objects.filter(id=permiso_id).first()
        if not permiso:
            return Response({"detail": "Permiso no encontrado"}, status=404)

        user.permissions.remove(permiso)
        return Response({"message": "Permiso removido correctamente"}, status=204)
