from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, userName, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(userName=userName, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userName, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(userName, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    idUser = models.AutoField(primary_key=True, unique=True)
    userName = models.CharField(max_length=50, unique=True)
    userRol = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    fdl = models.SmallIntegerField(default=0)  
    cbu = models.IntegerField(null=True, blank=True) 
    cat = models.DateTimeField(auto_now_add=True)  
    luu = models.IntegerField(null=True, blank=True)
    uat = models.DateTimeField(auto_now=True, null=True) 

    USERNAME_FIELD = 'userName'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.userName
