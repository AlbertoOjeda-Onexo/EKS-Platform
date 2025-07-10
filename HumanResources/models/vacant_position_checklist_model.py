from django.db import models
from .vacant_position_model import VacantPosition

VACANT_STATUS = (
    ("pendiente", "Pendiente"),
    ("aprobada", "Aprobada"),
    ("cerrada", "Cerrada")
)

class VacantPositionChecklist(models.Model):
    id = models.AutoField(primary_key=True)
    idVacantPosition = models.ForeignKey(VacantPosition, on_delete=models.CASCADE, related_name='checklist')
    title = models.CharField(max_length=255)
    description = models.TextField()
    fdl = models.SmallIntegerField(default=0)  
    cbu = models.IntegerField(null=True, blank=True) 
    cat = models.DateTimeField(auto_now_add=True)  
    luu = models.IntegerField(null=True, blank=True)
    uat = models.DateTimeField(auto_now=True, null=True) 

    def __str__(self):
        return self.titulo

