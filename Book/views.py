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
from .serializers import BookSerializer, PublisherSerializer, AuthorSerializer, CategorySerializer
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
    

class PublisherListView(APIView):
    def get(self, request):
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('size', 20)
        
        publishers = Publisher.objects.order_by('name')
        paginator = Paginator(publishers, page_size)

        try:
            publishers_page = paginator.page(page_number)
        except PageNotAnInteger:
            publishers_page = paginator.page(1)
        except EmptyPage:
            publishers_page = paginator.page(paginator.num_pages)

        serializer = PublisherSerializer(publishers_page, many=True)
        return Response(serializer.data)
    
    @api_view(['POST'])
    def post(self, request):
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PublisherDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Publisher, pk=pk)
    
    def get(self, request, pk):
        publisher = self.get_object(pk)
        serializer = PublisherSerializer(publisher)
        return Response(serializer.data)
    def put(self, request, pk):
        publisher = self.get_object(pk)
        serializer = PublisherSerializer(publisher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        publisher = self.get_object(pk)
        publisher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AuthorListView(APIView):
    def get(self, request):
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('size', 20)
        sort_by = request.GET.get('sort', 'name')
        sort_type = request.GET.get('type', 'asc')

        authors = Author.objects.all().order_by(f'{sort_by}' if sort_type == 'asc' else f'-{sort_by}')

        paginator = Paginator(authors, page_size)

        try:
            authors_page = paginator.page(page_number)
        except PageNotAnInteger:
            authors_page = paginator.page(1)
        except EmptyPage:
            authors_page = paginator.page(paginator.num_pages)

        serializers = AuthorSerializer(authors_page, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    

class AuthorDetailView(APIView):
    def get_object(self, id):
        return get_object_or_404(Author, id=id)

    def get(self, request, id):
        author = get_object_or_404(Author, id=id)
        serializers = AuthorSerializer(author)
        return Response(serializers.data)
    
    def put(self, request, id):
        author = self.get_object(id)
        serializers = AuthorSerializer(author, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        author = self.get_object(id)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AuthorCreateView(APIView):
    def post(self, request):
        serializers = AuthorSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(APIView):
    def get(self, request):
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('size', 20)
        sort_field = request.GET.get('sort', 'name')
        sort_type = request.GET.get('type', 'asc')

        categories = Category.objects.all().order_by(f"{sort_field}" if sort_type == 'asc' else f"-{sort_field}")
        paginator = Paginator(categories, page_size)

        try:
            categories_page = paginator.page(page_number)
        except PageNotAnInteger:
            categories_page = paginator.page(1)
        except EmptyPage:
            categories_page = paginator.page(paginator.num_pages)

        serializers = CategorySerializer(categories_page, many=True)
        return Response(serializers.data)
    
    def post(self, request):
        serializers = CategorySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CategoryDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)
    
    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        category = self.get_object(pk)
        serializers = CategorySerializer(category, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        
