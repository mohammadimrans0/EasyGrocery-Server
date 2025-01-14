from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Deposit, AddToCart, Checkout, PurchaseHistory, WishlistItem
from product.models import Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'price', 'stock']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'balance', 'contact_info', 'shopping_preferences']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        validated_data['balance'] = 0.00
        profile = super().create(validated_data)
        return profile


class DepositSerializer(serializers.ModelSerializer):
    user = User

    class Meta:
        model = Deposit
        fields = ['user', 'amount', 'created_at']


class AddToCartSerializer(serializers.ModelSerializer):
    user = User
    product = ProductSerializer()
    class Meta:
        model = AddToCart
        fields = ['id', 'user', 'product', 'quantity', 'added_at']


class CheckoutSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Checkout
        fields = ['id', 'user', 'total_amount', 'created_at']


class PurchaseHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductSerializer()
    class Meta:
        model = PurchaseHistory
        fields = ('id', 'user', 'product', 'purchased_at')


class WishlistItemSerializer(serializers.ModelSerializer):
    user = User
    product = ProductSerializer()
    class Meta:
        model = WishlistItem
        fields = ['id', 'user', 'product', 'added_at']

