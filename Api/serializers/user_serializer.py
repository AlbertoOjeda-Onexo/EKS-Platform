from datetime import datetime
from Api.models.user_model import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken, TokenError, RefreshToken, UntypedToken

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('idUser','userName', 'email', 'is_active')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('userName', 'email', 'password')
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener como mínimo 8 caracteres")
        return value

    def create(self, validated_data):

        request_user = self.context['request'].user

        if request_user.is_authenticated:
            user = User.objects.create_user(
                userName=validated_data['userName'],                
                email=validated_data['email'],
                password=validated_data['password'],
                cbu=request_user.id,
                luu=request_user.id
            )
        else:
            user = User.objects.create_user(
                userName=validated_data['userName'],                
                email=validated_data['email'],
                password=validated_data['password'],
                cbu=None,
                luu=None
            )
        return user
    
class LoginSerializer(serializers.Serializer):
    userName = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        userName = data['userName']
        password = data['password']
        
        user = User.objects.filter(userName=userName).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)    
            response_data= {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
                'user': user_serializer.data,
            }             
            return response_data
        raise ValidationError({"code":"Error de Autenticación","detail":"Credenciales incorrectas. Verifique usuario y contraseña."})  

class TokenValidatorSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        token = data['token']
        try:
            UntypedToken(token) 

            access_token = UntypedToken(token)
            user_id = access_token['user_id']

            user = User.objects.filter(idUser=user_id).first()
            if user:
                return {
                    'access_token': token,
                    'user': UserSerializer(user).data
                }
            else:
                raise serializers.ValidationError("Usuario no encontrado")
        except TokenError:
            raise serializers.ValidationError("Token inválido o expirado")