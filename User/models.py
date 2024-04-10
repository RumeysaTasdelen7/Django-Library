from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from django.core.exceptions import FieldError
from Book.models import Books
import re
from django_use_email_as_username.models import BaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=17, validators=[RegexValidator(regex=r'^\(\d{3}\) \d{3}-\d{4}$', message='Geçersiz phone formatı. Doğru format: (999) 999-9999')], blank=True)
    birthDate = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, max_length=80)
    createDate = models.DateField(default=timezone.now)
    resetPasswordCode = models.CharField(null=True, blank=True, max_length=50)
    builtIn = models.BooleanField(default=False)
    
    # Django'nun varsayılan is_staff ve is_superuser alanları
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'address', 'phone']  # Ek olarak gerekli alanlar

    class Meta:
        verbose_name_plural = 'Kullanıcılar'

    def __str__(self):
        return f"{self.firstName} - {self.lastName}"

class Role(models.Model):
    CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('member', 'Member'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, choices=CHOICES, unique=True, null=False)


class Loan(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    bookId = models.ForeignKey(Books, on_delete=models.CASCADE, null=False)
    loanDate = models.DateTimeField()
    expireData = models.DateTimeField()
    returnData = models.DateTimeField(null=True, blank=True)
    notes = models.CharField(max_length=300, null=True, blank=True)