from rest_framework import serializers
from .models import Loan, User, Role

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'userId', 'bookId', 'loanDate', 'expireData', 'returnData', 'notes']
