from .manager import UserManager
from django.contrib.auth.models import (
    AbstractBaseUser, Group, PermissionsMixin, Permission
)
from django.utils import timezone
from django.db import models

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Endereço de email', unique=True, blank=True, null=True)
    name = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    objects = UserManager()

    def __str__(self):
        return f'{self.name}'
