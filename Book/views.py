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
        

class BookDeleteView(APIView):
    def delete(self, request, id):
        book = Books.objects.get(pk=id)

        if book.loans.exists():
            return Response({'error': 'The book has related records in the loans table and cannot be deleted'}, status=status.HTTP_400_BAD_REQUEST)
        
        book.delete()
        serializers = BookSerializer(book)
        return Response(serializers.data, status=status.HTTP_200_OK)



# @api_view(['GET'])
# def books(request):
#     q = request.GET.get('q')
#     cat = request.GET.get('cat')
#     author = request.GET.get('author')
#     publisher = request.GET.get('publisher')
#     page = request.GET.get('page', 0)
#     size = request.GET.get('size', 20)
#     sort = request.GET.get('sort', 'name')
#     type = request.GET.get('type', 'asc')

#     if not q and not cat and not author and not publisher:
#         return Response({'error': 'At least one of the fields (q, cat, author and publisher) is required'}, status=status.HTTP_400_BAD_REQUEST)

#     q_obj = Q()
#     if q:
#         q_obj |= Q(name__icontains=q) | Q(isbn__icontains=q)
        
#     if cat:
#         q_obj &= Q(category_id=cat)
        
#     if author:
#         q_obj &= Q(author_id=author)
        
#     if publisher:
#         q_obj &= Q(publisher_id=publisher)
        
#     if not request.user.is_admin and 'active' in Books._meta.fields:
#         q_obj &= Q(active=True)
        
#     books = Books.objects.filter(q_obj).order_by(f'{sort}__{type}')

#     paginator = Paginator(books, size)
#     try:
#         books = paginator.page(page)
#     except PageNotAnInteger:
#         books = paginator.page(1)
#     except EmptyPage:
#         books = paginator.page(paginator.num_pages)
    
#     return Response({'books': [{'id': book.id, 'name': book.name, 'isbn': book.isbn} for book in books]}, status=status.HTTP_200_OK)


# def get_book(request, id):

#     book = Books.objects.filter(id=id).first()

#     if not book:
#         return JsonResponse({'error': 'Kitap bulunamadı.'}, status=404)
#     return JsonResponse({'id': book.id, 'name': book.name, 'isbn': book.isbn})


# def create_book(request):
#     if request.method == 'POST':
#         data = request.POST

#     if 'name' not in data or 'isbn' not in data or 'authorId' not in data or 'publisherId' not in data or 'categoryId' not in data or 'shelfCode' not in data or 'featured' not in data:
#         return JsonResponse({'error': 'name, isbn, authorId, publisherId, categoryId, shelfCode ve featured alanları gereklidir.'}, status=400)

#     if not re.match(r'^\d{3}-\d{2}-\d{5}-\d{2}-\d$', data['isbn']):
#         return JsonResponse({'error': 'Geçersiz ISBN formatı (Doğru format: 999-99-99999-99-9)'}, status=400)
    
#     if not re.match(r'^[A-Z]{2}-\d{3}$', data['shelfCode']):
#         return JsonResponse({'error': 'Geçersiz raf kodu formatı (Doğru format: AA-999)'}, status=400)

#     # Gerekli alanlar veritabanına kaydedilir
#     book = Books.objects.create(
#         name=data['name'],
#         isbn=data['isbn'],
#         pageCount=data.get('pageCount'),
#         authorId=data['authorId'],
#         publisherId=data['publisherId'],
#         publishDate=data.get('publishDate'),
#         categoryId=data['categoryId'],
#         image=data.get('image'),
#         shelfCode=data['shelfCode'],
#         featured=data['featured'],
#         active=True,
#         builtIn=False,
#         createDate=datetime.now(),
#         loanable=True
#     )

#     return JsonResponse({'id': book.id, 'name': book.name, 'isbn': book.isbn})

