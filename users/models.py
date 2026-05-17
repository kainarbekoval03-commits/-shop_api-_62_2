from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserConfirm(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='confirm')
    code = models.CharField(max_length=6)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.code}"
