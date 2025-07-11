from datetime import datetime
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models.candidate_model import Candidate, CustomFieldCandidate, CustomFieldValueCandidate

class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFieldCandidate
        fields = '__all__'

class CustomFieldValueSerializer(serializers.ModelSerializer):
    field = serializers.PrimaryKeyRelatedField(queryset=CustomFieldCandidate.objects.all(), write_only=True)    
    fieldID = serializers.IntegerField(source='field.idCustomField', read_only=True)
    fieldName = serializers.CharField(source='field.label', read_only=True)    
    
    class Meta:
        model = CustomFieldValueCandidate
        fields = ['field', 'fieldID', 'fieldName', 'value', 'file']
    
    def validate(self, data):
        field = data['field']
        value = data['value']
        
        if field.type == 'number':
            try:
                float(value)
            except ValueError:
                raise serializers.ValidationError({
                    "code": "Formato inválido",
                    "detail" :  f"El valor para el campo {field.label} debe ser un número válido"
                })              
        
        elif field.type == 'date':
            try:
                datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise serializers.ValidationError({
                    "code": "Formato inválido",
                    "detail" : f"El valor para el campo {field.label} debe ser una fecha válida en formato YYYY-MM-DD"
                })
        
        elif field.type == 'boolean':
            if value.lower() not in ['true', 'false', '1', '0', 'si', 'no']:
                raise serializers.ValidationError({
                    "code": "Formato inválido",
                    "detail" :  f"El valor para el campo {field.label} debe ser un valor booleano (true/false)"
                })             
        
        elif field.type == 'select':
            options = [opt.strip() for opt in field.options.split(',')] if field.options else []
            if value not in options:
                raise serializers.ValidationError({
                    "code": "Formato inválido",
                    "detail" :  f"El valor para el campo {field.label} debe ser una de estas opciones: {', '.join(options)}"
                })                             
        
        return data

class CandidateSerializer(serializers.ModelSerializer):
    valores_dinamicos = CustomFieldValueSerializer(many=True)
    vacantPositionTitle = serializers.CharField(source='idVacantPosition.title', read_only=True)
    
    class Meta:
        model = Candidate
        fields = ['idCandidate', 'idVacantPosition','vacantPositionTitle', 'name', 'firstSurName',  'secondSurName', 'status', 'valores_dinamicos']
        extra_kwargs = {
            'status': {'error_messages': {'invalid_choice': 'El status debe ser: pendiente, aprobado o rechazado'}}
        }

    def validate_idVacantPosition(self, value):
        if value.fdl == '1' or value.fdl == 1:
            raise serializers.ValidationError({
                "code": "Vacante Invalida",
                "detail": "La vacante seleccionada ya no se encuentra disponible."
            })
        return value

    def validate_status(self, value):
        from ..models.candidate_model import CANDIDATE_STATUS
        valid_statuses = [choice[0] for choice in CANDIDATE_STATUS]        
        if value not in valid_statuses:
            raise serializers.ValidationError({
                "code": "Status Invalido",
                "detail": f"El status debe ser alguna de las siguientes opciones: {', '.join(valid_statuses)}"
            })
        return value

    def validate(self, data):        
        required_fields = CustomFieldCandidate.objects.filter(required=True, fdl=0)
        submitted_fields = {v['field'].name for v in data.get('valores_dinamicos', [])}
        
        missing_fields = []
        for field in required_fields:
            if field.name not in submitted_fields:
                missing_fields.append(field.label)
        
        if missing_fields:
            raise serializers.ValidationError({
                "code": "Campos Faltantes",
                "detail": f"Los siguientes campos son obligatorios: {', '.join(missing_fields)}"
            })
        
        return data

    def create(self, validated_data):
        request_user = self.context['request'].user

        validated_data['cbu'] = request_user.idUser
        valores_dinamicos_data = validated_data.pop('valores_dinamicos')
        candidato = Candidate.objects.create(**validated_data)
        
        for valor_data in valores_dinamicos_data:
            field = valor_data['field']
            CustomFieldValueCandidate.objects.create(
                idCandidate=candidato,
                field=field,
                value=valor_data['value'],
                cbu = request_user.idUser
            )
        
        return candidato
    
class CustomFieldDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomFieldCandidate
        fields = ['fdl']

class CandidateDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = ['fdl']






