from rest_framework import serializers
from .models import Loan, User, Role
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'userId', 'bookId', 'loanDate', 'expireData', 'returnData', 'notes']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid Email or Password')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Both email and password are required')
        
    
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmPassword = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError({'password': 'Password fields did not match'})
        return attrs
    
    def create(self, validated_data):
        user = user.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    
    
class CustomUserSerializer(serializers.ModelSerializer):
    roles = serializers.ListField(
        child=serializers.CharField(max_length=100),
        allow_empty=False,
        required=False,
    )
    class Meta:
        model = User
        fields = '__all__'



    def to_representation(self, instance):
        data = super().to_representation(instance)
        roles_str = data.pop('roles')
        roles_list = "".join(roles_str).replace("[", "").replace("]", "").replace("'", "")
        roles_list = roles_list.split(",")
        data['roles'] = roles_list

        return data
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    old_password = serializers.CharField(write_only=True, required=True)
    confirmPassword = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'confirmPassword')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError({'password': 'Password fields did not match'})
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"oldpassword": "Old password is not correct"})
        
    def update(self, instance, validated_data):
        user_pk = self.context['request'].user.pk
        password = validated_data.pop('password')
        if user_pk == instance.pk:
            instance.set_password(password)
            instance.save()
        return instance
