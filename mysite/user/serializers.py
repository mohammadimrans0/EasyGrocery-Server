from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Deposit, AddToCart, Checkout, PurchaseHistory, WishlistItem
from django.core.exceptions import ObjectDoesNotExist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'image', 'balance', 'contact_info', 'shopping_preferences']

# Signup Serializer
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        # Check for unique username and email
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email is already registered."})
        return data

    def create(self, validated_data):
        # Remove confirm_password before creating the user
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
# login serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

# reset-password serializer
class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        # Check if user exists
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"username": "User does not exist."})

        # Check if passwords match
        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        return attrs

    def save(self, **kwargs):
        username = self.validated_data['username']
        new_password = self.validated_data['new_password']

        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()

        return user

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['user', 'amount', 'created_at']

class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddToCart
        fields = ['id', 'user', 'product', 'product_name', 'product_price', 'quantity', 'added_at']

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ['id', 'user', 'total_amount']
        

class PurchaseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHistory
        fields = ('id', 'user', 'product', 'purchased_at')

class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ['id', 'user', 'product', 'product_name']




"""
{
    "user": 1,
    "product": {
        "name": "Apple",
        "price": 350.00,
        "stock": 50
    }
}

"""