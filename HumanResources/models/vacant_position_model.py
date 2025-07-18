from django.db import models

TIPOS_CAMPO = (
    ("text", "Texto"),
    ("number", "Número"),
    ("date", "Fecha"),
    ("boolean", "Booleano"),
    ("select", "Selección"),
    ("file", "Archivo")
)

VACANT_STATUS = (
    ("pendiente", "Pendiente"),
    ("aprobada", "Aprobada"),
    ("cerrada", "Cerrada")
)

class VacantPosition(models.Model):
    idVacantPosition = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateField(null=True, blank=True)    
    status = models.CharField(max_length=20, choices=VACANT_STATUS)
    fdl = models.SmallIntegerField(default=0)  
    cbu = models.IntegerField(null=True, blank=True) 
    cat = models.DateTimeField(auto_now_add=True)  
    luu = models.IntegerField(null=True, blank=True)
    uat = models.DateTimeField(auto_now=True, null=True) 

    def __str__(self):
        return self.titulo

class CustomFieldVacantPosition(models.Model):
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

class CustomFieldValueVacantPosition(models.Model):
    idCustomFieldValue = models.AutoField(primary_key=True)
    idVacantPosition = models.ForeignKey(VacantPosition, on_delete=models.CASCADE, related_name="valores_dinamicos")
    field = models.ForeignKey(CustomFieldVacantPosition, on_delete=models.CASCADE)
    value = models.TextField()
    file = models.FileField(upload_to='uploads/vacant_position/', blank=True, null=True)
    fdl = models.SmallIntegerField(default=0)  
    cbu = models.IntegerField(null=True, blank=True) 
    cat = models.DateTimeField(auto_now_add=True)  
    luu = models.IntegerField(null=True, blank=True)
    uat = models.DateTimeField(auto_now=True, null=True)     

    def __str__(self):
        return f"{self.vacante.title} - {self.campo.label}: {self.valor}"
