from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager
from django.conf import settings
from django.utils import timezone


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
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=11)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    last_updated = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(Profile, self).save(*args, **kwargs)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='address', on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.address_line_1}, {self.city}'





