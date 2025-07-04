from django.db import models

class Profile(models.Model):
    idProfile = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    fdl = models.IntegerField(default=0, verbose_name='Flag Delete')
    cbu = models.IntegerField(verbose_name='Created By User')
    cat = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    luu = models.IntegerField(verbose_name='Last Update User')
    uat = models.DateTimeField(null=True, blank=True, verbose_name='Updated At')

    class Meta:
        db_table = 'profile'

    