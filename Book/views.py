import datetime
import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Books, Category, Author, Publisher
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from Book import serializers
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView

class BookFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name')
    author = filters.NumberFilter(field_name='author_id')
    category = filters.NumberFilter(field_name='category_id')
    publisher = filters.NumberFilter(field_name='publisher_id')

    class Meta:
        model = Books
        fields = ['name', 'author', 'category', 'publisher']

class BookListView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    filterset_class = BookFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.query_params.get('q')
        cat = self.request.query_params.get('cat')
        author = self.request.query_params.get('author')
        publisher = self.request.query_params.get('publisher')

        if not q and not cat and not author and not publisher:
            raise serializers.ValidationError("At least one of the fields (q, cat, author, and publisher) is required.")

        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(author__name__icontains=q) | Q(isbn__icontains=q) | Q(publisher__name__icontains=q))

        if cat:
            queryset = queryset.filter(category_id=cat)

        if author:
            queryset = queryset.filter(author_id=author)

        if publisher:
            queryset = queryset.filter(publisher_id=publisher)

        if not self.request.user.is_admin:
            queryset = queryset.filter(active=True)

        return queryset
    

class BookDetailView(APIView):
    def get(self, requset, id):
        book = get_object_or_404(Books, id=id)
        serializers = BookSerializer(book)
        return Response(serializers.data)
    


class BookCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class BookUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = Books.objects.get(pk=book_id)
        serializers = BookSerializer(book, data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, id):
        book = get_object_or_404(Books, id=id)
        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             

class BookDeleteView(DestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Book deleted succesfully", "success": True})
    