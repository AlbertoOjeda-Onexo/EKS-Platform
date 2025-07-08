from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ..models.vacant_position_model import VacantPosition, CustomField, CustomFieldValue
from ..serializers.vacant_position_serializer import VacantPositionSerializer, CustomFieldSerializer, CustomFieldDeleteSerializer

class CustomFieldListCreateView(generics.ListCreateAPIView):    
    queryset = CustomField.objects.filter(fdl=0)
    serializer_class = CustomFieldSerializer


class VacantPositionListCreateView(generics.ListCreateAPIView):    
    queryset = VacantPosition.objects.all()
    serializer_class = VacantPositionSerializer

class CustomFieldDeleteView(generics.DestroyAPIView):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldDeleteSerializer  

    def perform_destroy(self, instance):
        instance.fdl = 1
        instance.save()

    def delete(self, request, *args, **kwargs):        
        self.perform_destroy(self.get_object())
        return Response({
            "code": "Vacante eliminada",
            "detail": "La vacante se ha eliminado exitosamente."
        }, status=status.HTTP_204_NO_CONTENT)