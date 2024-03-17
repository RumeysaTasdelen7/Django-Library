from django.urls import path
from .views import LoanListView, LoanDetailView, UserLoanListView, BookLoanListView, AuthLoanDetailView

urlpatterns = [
    path('loans/', LoanListView.as_view(), name='loan-list'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('loans/user/<str:userId>/', UserLoanListView.as_view(), name='user-loans'),
    path('loans/book/<str:bookId>/', BookLoanListView.as_view(), name='book-loans'),
    path('loans/auth/<str:loanId>/', AuthLoanDetailView.as_view(), name='auth_loan_detail'),
]