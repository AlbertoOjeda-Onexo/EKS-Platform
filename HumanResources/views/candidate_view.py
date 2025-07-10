from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from Api.models.permission_model import HasCustomPermission
from ..models.candidate_model import Candidate, CustomFieldCandidate, CustomFieldValueCandidate
from ..serializers.candidate_serializer import CandidateSerializer, CustomFieldSerializer, CustomFieldDeleteSerializer, CandidateDeleteSerializer

class CustomFieldCandidateListCreateView(generics.ListCreateAPIView):    
    queryset = CustomFieldCandidate.objects.filter(fdl=0)
    serializer_class = CustomFieldSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), HasCustomPermission()]
        return [IsAuthenticated()]
    
    required_permission = "crear_campo_dinamico"

class CandidateListCreateView(generics.ListCreateAPIView):    
    queryset = Candidate.objects.filter(fdl=0)
    serializer_class = CandidateSerializer

    def get_permissions(self):
        if self.request.method == "POST":            
            return [IsAuthenticated(), HasCustomPermission()]
        return [IsAuthenticated()]  

    required_permission = "crear_candidato"

class CustomFieldCandidateDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permission = 'borrar_campo_dinamico'
    queryset = CustomFieldCandidate.objects.all()
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
    
class CandidateDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permission = 'eliminar_candidato'    
    queryset = Candidate.objects.all()
    serializer_class = CandidateDeleteSerializer  

    def perform_destroy(self, instance):
        request_user = self.request.user
        instance.fdl = 1
        instance.luu = request_user.idUser
        instance.save()

    def delete(self, request, *args, **kwargs):        
        self.perform_destroy(self.get_object())
        return Response({
            "code": "Candidato eliminado",
            "detail": "El candidato se ha eliminado exitosamente."
        }, status=status.HTTP_204_NO_CONTENT)
    
class CandidateApproveView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permission = 'aceptar_candidato'

    queryset = Candidate.objects.all()
    serializer_class = CandidateDeleteSerializer  

    def perform_update(self, instance):
        request_user = self.request.user
        instance.status = 'aprobado'
        instance.luu = request_user.idUser
        instance.save()

    def patch(self, request, *args, **kwargs):        
        self.perform_update(self.get_object())
        return Response({
            "code": "Candidato aprovado.",
            "detail": "El candidato ha sido aprovado exitosamente."
        }, status=status.HTTP_204_NO_CONTENT)