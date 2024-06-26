from django.shortcuts import render
from rest_framework.views import APIView
from .models import Loan, User
from .serializers import LoanSerializer, RegisterSerializer, CustomLoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import filters
from core.page_filter import pages_filter

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({'message': 'Registration succesfully done.', 'success':True})
    

class LoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        access_token = str(AccessToken.for_user(user))

        return Response({"token": access_token})
    


class UserView(ListAPIView):
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["firstName", "lastName"]

    def  get_queryset(self):
        queryset = User.objects.all()

        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        return queryset
        
    def list(self, request, *args, **kwargs):
        if request.path.startswith('user/auth/pages') or request.path.startswith('/user/auth/pages'):
            return pages_filter(self, request, User, *args, **kwargs)
        return super().list(request, *args, **kwargs)

class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    


class LoanListView(APIView):
    def get(self, request):
        loans = Loan.objects.all()

        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LoanCreateView(APIView):
    def post(self, request):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoanDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Loan, pk=pk)
    
    def  get(self, request, pk):
        loan = self.get_object(pk)
        serializer = LoanSerializer(loan)
        serializer.data.pop('notes', None)
        return Response(serializer.data)
    
    def put(self, request, pk):
        loan = self.get_object(pk)
        serializer = LoanSerializer(loan, data=request.data)
        if serializer.is_valid():

            if 'returnDate' in request.data and request.data['returnDate']:

                loan.bookId.loanable = True
                loan.bookId.save()

                loan.returnDate = request.data['returnDate']
                if loan.returnDate <= loan.expireDate:
                    loan.userId.score += 1
                else:
                    loan.userId.score -= 1
                loan.userId.save()
            else:
                loan.notes = request.data.get('notes', loan.notes)
                loan.expireDate = request.data.get('expireDate', loan.expireDate)
            loan.save()
            return Response(LoanSerializer(loan).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        loan = self.get_object(pk)
        loan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UserLoanListView(APIView):
    def get(self, request, userId):
        user_loans = Loan.objects.filter(userId=userId)

        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('size', 20)
        paginator = Paginator(user_loans, page_size)

        try:
            loans_page = paginator.page(page_number)
        except PageNotAnInteger:
            loans_page = paginator.page(1)
        except EmptyPage:
            loans_page = paginator.page(paginator.num_pages)


        serializer = LoanSerializer(loans_page, many=True)

        for loan_data in serializer.data:
            loan_data.pop('notes', None)

        return Response(serializer.data)
    

class BookLoanListView(APIView):
    def get(self, request, bookId):
        book_loans = Loan.objects.filter(bookId=bookId)

        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('size', 20)
        paginator = Paginator(book_loans, page_size)

        try:
            loans_page = paginator.page(page_number)
        except PageNotAnInteger:
            loans_page = paginator.page(1)
        except EmptyPage:
            loans_page = paginator.page(paginator.num_pages)


        serializer = LoanSerializer(loans_page, many=True)

        for loan_data in serializer.data:
            loan_data.pop('notes', None)
            user_id = loan_data['userId']
            user = User.objects.get(id=user_id)
            loan_data['user'] = {
                'id': user_id,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'address': user.address,
                'phone': user.phone,
                'birthDate': user.birthDate,
                'email': user.email,
                'createDate': user.createDate,
                'resetPasswordCode': user.resetPasswordCode,
                'builtIn': user.builtIn,
            }

        return Response(serializer.data)
    

class AuthLoanDetailView(APIView):
    def get(self, request, loanId):
        loan = get_object_or_404(Loan, pk=loanId)
        

        serializer = LoanSerializer(loan)

        user_data = {
            'id': loan.userId.id,
            'firstName': loan.userId.firstName,
            'lastName': loan.userId.lastName,
            'address': loan.userId.address,
            'phone': loan.userId.phone,
            'birthDate': loan.userId.birthDate,
            'email': loan.userId.email,
            'createDate': loan.userId.createDate,
            'resetPasswordCode': loan.userId.resetPasswordCode,
            'builtIn': loan.userId.builtIn,
        }

        book_data = {
            'id': loan.bookId.id,
            'name': loan.bookId.name,
            'isbn': loan.bookId.isbn,
            'pageCount': loan.bookId.pageCount,
            'sort': loan.bookId.sort,
            'authorId': loan.bookId.authorId.id,
            'publisherId': loan.bookId.publisherId.id,
            'publishDate': loan.bookId.publishDate,
            'categoryId': loan.bookId.categoryId.id,
            'image': str(loan.bookId.image),
            'loanable': loan.bookId.loanable,
            'shelfCode': loan.bookId.shelfCode,
            'active': loan.bookId.active,
            'featured': loan.bookId.featured,
            'createDate': loan.bookId.createDate,
            'builtIn': loan.bookId.builtIn,
        }

        response_data = {
            'id': loan.id,
            'userId': loan.userId.id,
            'bookId': loan.bookId.id,
            'book': book_data,
            'user': user_data,
        }

        return Response(response_data)



