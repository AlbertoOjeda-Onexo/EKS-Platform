from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ..models.vacant_position_model import VacantPosition, CustomField, CustomFieldValue
from ..serializers.vacant_position_serializer import VacantPositionSerializer, CustomFieldSerializer, CustomFieldDeleteSerializer, VacantPositionDeleteSerializer

class CustomFieldListCreateView(generics.ListCreateAPIView):    
    queryset = CustomField.objects.filter(fdl=0)
    serializer_class = CustomFieldSerializer

class VacantPositionListCreateView(generics.ListCreateAPIView):    
    queryset = VacantPosition.objects.filter(fdl=0)
    serializer_class = VacantPositionSerializer

class CustomFieldDeleteView(generics.DestroyAPIView):
    queryset = CustomField.objects.all()
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