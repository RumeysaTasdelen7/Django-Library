from django.contrib import admin
from .models import Books, Category, Author, Publisher

# Register your models here.

admin.site.register(Books)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Publisher)