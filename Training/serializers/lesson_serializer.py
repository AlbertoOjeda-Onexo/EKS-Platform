import json
from datetime import datetime
from django.db import transaction
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models.lesson_model import Lesson, CustomFieldLesson, CustomFieldValueLesson

class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFieldLesson
        fields = '__all__'

class CustomFieldValueSerializer(serializers.ModelSerializer):
    field = serializers.PrimaryKeyRelatedField(queryset=CustomFieldLesson.objects.all(), write_only=True)    
    fieldID = serializers.IntegerField(source='field.idCustomField', read_only=True)
    fieldName = serializers.CharField(source='field.label', read_only=True)    
    
    class Meta:
        model = CustomFieldValueLesson
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
                    "detail": f"El valor para el campo {field.label} debe ser un número válido"
                })              
        
        elif field.type == 'date':
            try:
                datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise serializers.ValidationError({
                    "code": "Formato inválido",
                    "detail": f"El valor para el campo {field.label} debe ser una fecha válida en formato YYYY-MM-DD"
                })
        
        elif field.type == 'boolean':
            if value.lower() not in ['true', 'false', '1', '0', 'si', 'no']:
                raise serializers.ValidationError({
                    "code": "Formato inválido",
                    "detail": f"El valor para el campo {field.label} debe ser un valor booleano (true/false)"
                })             
        
        elif field.type == 'select':
            options = [opt.strip() for opt in field.options.split(',')] if field.options else []
            if value not in options:
                raise serializers.ValidationError({
                    "code": "Formato inválido",
                    "detail": f"El valor para el campo {field.label} debe ser una de estas opciones: {', '.join(options)}"
                })                             
        
        return data

class LessonSerializer(serializers.ModelSerializer):
    valores_dinamicos = serializers.JSONField(write_only=True)  
    dynamic_values = CustomFieldValueSerializer(
        source='valores_dinamicos', 
        many=True, 
        read_only=True
    )    
    
    class Meta:
        model = Lesson
        fields = [ 'idLesson', 'title', 'description', 'duration', 'status', 'valores_dinamicos', 'dynamic_values']
        extra_kwargs = {
            'status': {'error_messages': {'invalid_choice': 'El status debe ser: pendiente, aprobado o archivado'}}
        }

    def validate_valores_dinamicos(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError("El campo valores_dinamicos debe ser un JSON válido")
        
        if not isinstance(value, list):
            raise serializers.ValidationError("El campo valores_dinamicos debe ser una lista de objetos")
        
        return value

    def validate_status(self, value):
        from ..models.lesson_model import LESSON_STATUS
        valid_statuses = [choice[0] for choice in LESSON_STATUS]        
        if value not in valid_statuses:
            raise serializers.ValidationError({
                "code": "Status Invalido",
                "detail": f"El status debe ser alguna de las siguientes opciones: {', '.join(valid_statuses)}"
            })
        return value

    def validate(self, data):        
        required_fields = CustomFieldLesson.objects.filter(required=True, fdl=0)
        valores_dinamicos = data.get('valores_dinamicos', [])

        # Obtener el JSON de los metadatos y convertirlo en Python
        files_metadata_json = self.context['request'].data.get('files_metadata')
        try:
            files_metadata = json.loads(files_metadata_json) if files_metadata_json else []
        except json.JSONDecodeError:
            raise serializers.ValidationError({
                "files_metadata": "El JSON de los metadatos de archivos es inválido."
            })

        # Recolectar todos los IDs de campos enviados
        submitted_fields = {v['field'] for v in valores_dinamicos if 'field' in v}
        submitted_fields.update({v['field'] for v in files_metadata if 'field' in v})

        # Verificar campos requeridos
        missing_fields = []
        for field in required_fields:
            if field.idCustomField not in submitted_fields:
                missing_fields.append(field.name)
        
        if missing_fields:
            raise serializers.ValidationError({
                "code": "Campos Faltantes",
                "detail": f"Los siguientes campos son obligatorios: {', '.join(missing_fields)}"
            })
        
        dynamic_fields = CustomFieldLesson.objects.filter(fdl=0)
        field_dict = {field.idCustomField: field for field in dynamic_fields}
        
        for item in valores_dinamicos:
            field_id = item.get('field')
            if field_id not in field_dict:
                raise serializers.ValidationError({
                    "code": "Campo no encontrado",
                    "detail": f"No existe un campo dinámico con ID {field_id}"
                })
            
            field = field_dict[field_id]
            value = item.get('value', '')
        
        return data

    def create(self, validated_data):
        request_user = self.context['request'].user
        valores_dinamicos_data = validated_data.pop('valores_dinamicos')
        files_metadata_json = self.context['request'].data.get('files_metadata')

        with transaction.atomic():  
            # Crear la clase
            validated_data['cbu'] = request_user.idUser
            clase = Lesson.objects.create(**validated_data)

            try:
                files_metadata = json.loads(files_metadata_json) if files_metadata_json else []
            except json.JSONDecodeError:
                raise serializers.ValidationError({
                    "files_metadata": "El JSON de los metadatos de archivos es inválido."
                })

            # Asociar archivos con campos dinámicos
            for meta in files_metadata:                
                field_id = meta.get('field')
                file_name = meta.get('filename')
                field_name = meta.get('fieldName')  # Nombre del campo en el formData
                if field_name:
                    file_obj = self.context['request'].FILES.get(field_name)
                    if file_obj:
                        CustomFieldValueLesson.objects.create(
                            idLesson=clase,
                            field_id=field_id,
                            value=file_name,
                            file=file_obj,
                            cbu=request_user.idUser
                        )

            # Crear los valores dinámicos
            for valor_data in valores_dinamicos_data:
                field_id = valor_data['field']
                field = CustomFieldLesson.objects.get(idCustomField=field_id)

                CustomFieldValueLesson.objects.create(
                    idLesson=clase,
                    field=field,
                    value=valor_data.get('value', ''),
                    cbu=request_user.idUser
                )

        return clase


class CustomFieldDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFieldLesson
        fields = ['fdl']

class LessonDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['fdl']