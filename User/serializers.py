from rest_framework import serializers
from .models import Loan, User, Role
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'userId', 'bookId', 'loanDate', 'expireData', 'returnData', 'notes']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("id", "firstName", "lastName", "password", "address", "phone", "builtIn", "email")
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid Email or Password')
            attrs['user'] = user  # Kullanıcıyı validated_data içine ekleyin
            return attrs
        else:
            raise serializers.ValidationError('Both email and password are required')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'