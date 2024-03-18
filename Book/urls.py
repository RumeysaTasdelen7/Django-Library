from django.urls import path
from .views import BookCreateView, BookListView, BookDetailView, BookUpdateView, BookDeleteView, PublisherListView, PublisherDetailView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:id>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:id>/', BookDeleteView.as_view(), name='book-delete'),
    path('publishers/', PublisherListView.as_view(), name='publisher-list'),
    path('publishers/<int:pk>/', PublisherDetailView.as_view(), name='publisher-detail')
]