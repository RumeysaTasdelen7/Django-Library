from django.urls import path
from .views import LoanListView, LoanCreateView, LoanDetailView, UserLoanListView, BookLoanListView, AuthLoanDetailView, RegisterView, LoginView, UserView, UserDetailView

urlpatterns = [
    path('loans/', LoanListView.as_view(), name='loan-list'),
    path('loans/create/', LoanCreateView.as_view(), name='loan-create'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('loans/user/<str:userId>/', UserLoanListView.as_view(), name='user-loans'),
    path('loans/book/<str:bookId>/', BookLoanListView.as_view(), name='book-loans'),
    path('loans/auth/<str:loanId>/', AuthLoanDetailView.as_view(), name='auth_loan_detail'),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path('user/', UserView.as_view(), name='user'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail')
]