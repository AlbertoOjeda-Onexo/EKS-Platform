from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from Api.models.permission_model import HasCustomPermission
from rest_framework.parsers import MultiPartParser, FormParser
from ..models.lesson_model import Lesson, CustomFieldLesson, CustomFieldValueLesson
from ..serializers.lesson_serializer import LessonSerializer, CustomFieldSerializer, CustomFieldDeleteSerializer, LessonDeleteSerializer

class CustomFieldLessonListCreateView(generics.ListCreateAPIView):    
    queryset = CustomFieldLesson.objects.filter(fdl=0)
    serializer_class = CustomFieldSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), HasCustomPermission()]
        return [IsAuthenticated()]
    
    required_permission = "crear_campo_dinamico"

class LessonListCreateView(generics.ListCreateAPIView):    
    queryset = Lesson.objects.filter(fdl=0)
    serializer_class = LessonSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == "POST":            
            return [IsAuthenticated(), HasCustomPermission()]
        return [IsAuthenticated()]  

    required_permission = "crear_clase"

class CustomFieldLessonDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permission = 'borrar_campo_dinamico'
    queryset = CustomFieldLesson.objects.all()
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
    
class LessonDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permission = 'eliminar_clase'    
    queryset = Lesson.objects.all()
    serializer_class = LessonDeleteSerializer  

    def perform_destroy(self, instance):
        request_user = self.request.user
        instance.fdl = 1
        instance.luu = request_user.idUser
        instance.save()

    def delete(self, request, *args, **kwargs):        
        self.perform_destroy(self.get_object())
        return Response({
            "code": "Clase eliminada",
            "detail": "La clase se ha eliminado exitosamente."
        }, status=status.HTTP_204_NO_CONTENT)
    
class LessonApproveView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasCustomPermission]
    required_permission = 'aprobar_clase'

    queryset = Lesson.objects.all()
    serializer_class = LessonDeleteSerializer  

    def perform_update(self, instance):
        request_user = self.request.user
        instance.status = 'aprobada'
        instance.luu = request_user.idUser
        instance.save()

    def patch(self, request, *args, **kwargs):        
        self.perform_update(self.get_object())
        return Response({
            "code": "Clase aprovada.",
            "detail": "La clase ha sido aprovada exitosamente."
        }, status=status.HTTP_204_NO_CONTENT)