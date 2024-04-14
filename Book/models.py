from django.db import models
from django.core.exceptions import ValidationError
import re

class Books(models.Model):
    name = models.CharField(max_length=80, null=False)
    isbn = models.CharField(max_length=17, null=False)

    def clean(self):
        if not re.match(r'^\d{3}-\d{2}-\d{5}-\d{2}-\d$', self.isbn):
            raise ValidationError('Geçersiz ISBN formatı (Doğru format: 999-99-99999-99-9)')
        
    pageCount = models.IntegerField(null=True, blank=True)
    sort = models.CharField(max_length=20, null=False, default='name')
    authorId = models.ForeignKey('Author', null=False, on_delete=models.CASCADE)
    publisherId = models.ForeignKey('Publisher', null=False, on_delete=models.CASCADE)
    publishDate = models.IntegerField(null=True, blank=True)
    categoryId = models.ForeignKey('Category', null=False, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    loanable = models.BooleanField(null=False, default=True)
    shelfCode = models.CharField(max_length=10, help_text="Format: WF-214")

    def clean_shelf_code(self):
        if not re.match(r'^[A-Z]{2}-\d{3}$', self.shelfCode):
            raise ValidationError('Geçersiz raf kodu formatı (Doğru format: AA-999)')
        
    active = models.BooleanField(null=False, default=True)
    featured = models.BooleanField(null=False, default=False)
    createDate = models.DateTimeField(null=False, auto_now_add=True)
    builtIn = models.BooleanField(null=False, default=False)

    class Meta:
        verbose_name_plural = 'Kitaplar'
        
    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=80, null=False)
    builtIn = models.BooleanField(null=False, default=False)
    sequence = models.IntegerField(null=False, default=0)

    class Meta:
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return f"{self.name}"
    

class Author(models.Model):
    name = models.CharField(null=False, max_length=70)
    builtIn = models.BooleanField(null=False, max_length=70)

    class Meta:
        verbose_name_plural = 'Yazarlar'

    def __str__(self):
        return f"{self.name}"
    
class Publisher(models.Model):
    name = models.CharField(null=False, max_length=70)
    builtIn = models.BooleanField(null=False, default=False)

    class Meta:
        verbose_name_plural = 'Yayınevleri'
        
    def __str__(self):
        return f"{self.name}"
