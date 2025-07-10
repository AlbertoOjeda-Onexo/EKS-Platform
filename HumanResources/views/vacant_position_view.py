from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from Api.models.permission_model import HasCustomPermission
from ..models.vacant_position_model import VacantPosition, CustomFieldVacantPosition, CustomFieldValueVacantPosition
from ..serializers.vacant_position_serializer import VacantPositionSerializer, CustomFieldSerializer, CustomFieldDeleteSerializer, VacantPositionDeleteSerializer

class CustomFieldVacantPositionListCreateView(generics.ListCreateAPIView):    
    queryset = CustomFieldVacantPosition.objects.filter(fdl=0)
    serializer_class = CustomFieldSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), HasCustomPermission()]
        return [IsAuthenticated()]
    
    required_permission = "crear_campo_dinamico"

class VacantPositionListCreateView(generics.ListCreateAPIView):    
    queryset = VacantPosition.objects.filter(fdl=0)
    serializer_class = VacantPositionSerializer

    def get_permissions(self):
        if self.request.method == "POST":            
            return [IsAuthenticated(), HasCustomPermission()]
        return [IsAuthenticated()]  

    required_permission = "crear_vacante"

class CustomFieldVacantPositionDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permission = 'borrar_campo_dinamico'
    queryset = CustomFieldVacantPosition.objects.all()
    serializer_class = CustomFieldDeleteSerializer  

    def perform_destroy(self, instance):
        request_user = self.request.user
        instance.fdl = 1
        instance.luu = request_user.idUser
        instance.save()

    def delete(self, request, *args, **kwargs):        
        self.perform_destroy(self.get_object())
        return Response({
            "code": "Campo eliminado.",
            "detail": "El campo personalizado se ha eliminado exitosamente."
        }, status=status.HTTP_204_NO_CONTENT)
    
class VacantPositionDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permission = 'eliminar_vacante'    
    queryset = VacantPosition.objects.all()
    serializer_class = VacantPositionDeleteSerializer  

    def perform_destroy(self, instance):
        request_user = self.request.user
        instance.fdl = 1
        instance.luu = request_user.idUser
        instance.save()

    def delete(self, request, *args, **kwargs):        
        self.perform_destroy(self.get_object())
        return Response({
            "code": "Vacante eliminada",
            "detail": "La vacante se ha eliminado exitosamente."
        }, status=status.HTTP_204_NO_CONTENT)
    
class VacantPositionApproveView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permission = 'aprobar_vacante'

    queryset = VacantPosition.objects.all()
    serializer_class = VacantPositionDeleteSerializer  

    def perform_update(self, instance):
        request_user = self.request.user
        instance.status = 'aprobada'
        instance.luu = request_user.idUser
        instance.save()

    def patch(self, request, *args, **kwargs):        
        self.perform_update(self.get_object())
        return Response({
            "code": "Vacante aprovada.",
            "detail": "La vacante ha sido aprovada exitosamente."
        }, status=status.HTTP_204_NO_CONTENT)