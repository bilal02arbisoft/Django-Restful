from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):

        return self.user.email

    def save(self, *args, **kwargs):

        self.full_name = f'{self.user.first_name} {self.user.last_name}'
        self.last_updated = timezone.now()
        super(Profile, self).save(*args, **kwargs)


