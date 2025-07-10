from datetime import datetime
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models.vacant_position_checklist_model import VacantPositionChecklist

class VacantPositionCheckListSerializer(serializers.ModelSerializer):    
    
    class Meta:
        model = VacantPositionChecklist
        fields = '__all__'

    def validate_idVacantPosition(self, value):
        if value.fdl == '1' or value.fdl == 1:
            raise serializers.ValidationError({
                "code": "Vacante Invalida",
                "detail": "La vacante seleccionada ya no se encuentra disponible."
            })
        return value

    def create(self, validated_data):
        request_user = self.context['request'].user

        validated_data['cbu'] = request_user.idUser        
        checklist = VacantPositionChecklist.objects.create(**validated_data)
        
        return checklist
    
class VacantPositionCheckListDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = VacantPositionChecklist
        fields = ['fdl']