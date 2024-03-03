from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from django.core.exceptions import FieldError
from Book.models import Books
import re

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=17)
    firstName = models.CharField(max_length=30, null=False, blank=False)
    lastName = models.CharField(max_length=30, null=False)
    score = models.IntegerField(null=False, default=0)
    address = models.CharField(null=False, max_length=100)
    phone = models.CharField(null=False, max_length=12)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)
        if not re.match(r'^\d{3}-\d{2}-\d{5}-\d{2}-\d$', self.phone):
            raise FieldError({'phone': ['Geçersiz phone formatı (Doğru format: 999-99-99999-99-9)']})

    # def clean(self):
    #     if not re.match(r'^\d{3}-\d{2}-\d{5}-\d{2}-\d$', self.phone):
    #         raise ValidationError('Geçersiz phone formatı (Doğru format: 999-99-99999-99-9)')
        
    birthDate = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=80, null=False)
    password = models.CharField(max_length=128, null=False)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    createDate = models.DateField(null=False)
    resetPasswordCode = models.CharField(null=True, blank=True, max_length=50)
    builtIn = models.BooleanField(null=False, default=False)

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