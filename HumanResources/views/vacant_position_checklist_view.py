from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from Api.models.permission_model import HasCustomPermission
from ..models.vacant_position_checklist_model import VacantPositionChecklist
from ..serializers.vacant_position_checklist_serializer import VacantPositionCheckListSerializer, VacantPositionCheckListDeleteSerializer

class VacantPositionCheckListCreateView(generics.ListCreateAPIView):    
    queryset = VacantPositionChecklist.objects.filter(fdl=0)
    serializer_class = VacantPositionCheckListSerializer

    def get_permissions(self):
        if self.request.method == "POST":            
            return [IsAuthenticated(), HasCustomPermission()]
        return [IsAuthenticated()]  
    
    def get_queryset(self):
        queryset = VacantPositionChecklist.objects.filter(fdl=0)
        idVacantPosition = self.request.query_params.get("idVacantPostion")
        if idVacantPosition:
            queryset = queryset.filter(idVacantPosition=idVacantPosition)
        return queryset

    required_permission = "aprobar_vacante"

class VacantPositionCheckDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permission = 'aprobar_vacante'    
    queryset = VacantPositionChecklist.objects.all()
    serializer_class = VacantPositionCheckListDeleteSerializer  

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
    