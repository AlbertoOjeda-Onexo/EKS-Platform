from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Api.models.permission_model import CustomPermission

class CustomPermissionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        permisos = CustomPermission.objects.all().values("id", "code", "description")
        return Response(permisos, status=200)

    def post(self, request):
        code = request.data.get("code")
        description = request.data.get("description", "")

        if not code:
            return Response({"error": "El campo 'code' es obligatorio."}, status=400)

        if CustomPermission.objects.filter(code=code).exists():
            return Response({"error": "Ya existe un permiso con ese código."}, status=400)

        permiso = CustomPermission.objects.create(code=code, description=description)
        return Response({
            "message": "Permiso creado correctamente",
            "id": permiso.id,
            "code": permiso.code,
            "description": permiso.description
        }, status=201)
