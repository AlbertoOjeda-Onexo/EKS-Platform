from django.db import models

TIPOS_CAMPO = (
    ("text", "Texto"),
    ("number", "Número"),
    ("date", "Fecha"),
    ("boolean", "Booleano"),
    ("select", "Selección"),
    ("file", "Archivo")
)

LESSON_STATUS = (
    ("pendiente", "Pendiente"),
    ("aprobada", "Aprobada"),
    ("archivada", "Archivada")
)

class Lesson(models.Model):
    idLesson = models.AutoField(primary_key=True)    
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=LESSON_STATUS)
    fdl = models.SmallIntegerField(default=0)  
    cbu = models.IntegerField(null=True, blank=True) 
    cat = models.DateTimeField(auto_now_add=True)  
    luu = models.IntegerField(null=True, blank=True)
    uat = models.DateTimeField(auto_now=True, null=True) 

    def __str__(self):
        return self.titulo

class CustomFieldLesson(models.Model):
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

class CustomFieldValueLesson(models.Model):
    idCustomFieldValue = models.AutoField(primary_key=True)
    idLesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="valores_dinamicos")
    field = models.ForeignKey(CustomFieldLesson, on_delete=models.CASCADE)
    value = models.TextField()
    file = models.FileField(upload_to='lessons/', blank=True, null=True)
    fdl = models.SmallIntegerField(default=0)  
    cbu = models.IntegerField(null=True, blank=True) 
    cat = models.DateTimeField(auto_now_add=True)  
    luu = models.IntegerField(null=True, blank=True)
    uat = models.DateTimeField(auto_now=True, null=True)     

    def __str__(self):
        return f"{self.clase.name} - {self.campo.label}: {self.valor}"
