from rest_framework import serializers
from .models import  Category, Author, Publisher, Books

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'builtIn']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'builtIn']