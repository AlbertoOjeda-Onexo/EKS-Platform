from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from Api.models.user_model import User
from Api.serializers.user_serializer import RegisterSerializer, UserSerializer, LoginSerializer, TokenValidatorSerializer


class RegisterView(APIView):

    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

    permission_classes = [AllowAny] 
    
    def get(self, request, idUser):
        instance = User.objects.filter(idUser = idUser)
        if not instance:
            return Response({"error": "user not fonund"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ValidateTokenView(APIView):
    
    def post(self, request):
        serializer = TokenValidatorSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):

    def post(self, request,idUser=None):
        user = request.user
        
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"error": "Debes proporcionar la contraseña actual y la nueva."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"error": "La contraseña actual es incorrecta."},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Contraseña cambiada correctamente."}, status=status.HTTP_200_OK)