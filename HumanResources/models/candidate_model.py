from django.db import models
from ..models.vacant_position_model import VacantPosition

TIPOS_CAMPO = (
    ("text", "Texto"),
    ("number", "Número"),
    ("date", "Fecha"),
    ("boolean", "Booleano"),
    ("select", "Selección"),
    ("file", "Archivo")
)

CANDIDATE_STATUS = (
    ("pendiente", "Pendiente"),
    ("aprobado", "Aprobado"),
    ("rechazado", "Rechazado")
)

class Candidate(models.Model):
    idCandidate = models.AutoField(primary_key=True)
    idVacantPosition = models.ForeignKey(VacantPosition, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=255)
    firstSurName = models.CharField(max_length=255)
    secondSurName = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=CANDIDATE_STATUS)
    fdl = models.SmallIntegerField(default=0)  
    cbu = models.IntegerField(null=True, blank=True) 
    cat = models.DateTimeField(auto_now_add=True)  
    luu = models.IntegerField(null=True, blank=True)
    uat = models.DateTimeField(auto_now=True, null=True) 

    def __str__(self):
        return self.titulo

class CustomFieldCandidate(models.Model):
    idCustomField = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TIPOS_CAMPO)
    options = models.TextField(null=True, blank=True, help_text="Solo para campos tipo 'select', separadas por comas.")
    required = models.BooleanField(default=False)
    fdl = models.SmallIntegerField(default=0)  
    cbu = models.IntegerField(null=True, blank=True) 
    cat = models.DateTimeField(auto_now_add=True)  
    luu = models.IntegerField(null=True, blank=True)
    uat = models.DateTimeField(auto_now=True, null=True)     

    def __str__(self):
        return self.label

class CustomFieldValueCandidate(models.Model):
    idCustomFieldValue = models.AutoField(primary_key=True)
    idCandidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="valores_dinamicos")
    field = models.ForeignKey(CustomFieldCandidate, on_delete=models.CASCADE)
    value = models.TextField()
    file = models.FileField(upload_to='uploads/candidates/', blank=True, null=True)
    fdl = models.SmallIntegerField(default=0)  
    cbu = models.IntegerField(null=True, blank=True) 
    cat = models.DateTimeField(auto_now_add=True)  
    luu = models.IntegerField(null=True, blank=True)
    uat = models.DateTimeField(auto_now=True, null=True)     

    def __str__(self):
        return f"{self.candidato.name} - {self.campo.label}: {self.valor}"
