from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Deposit, AddToCart, Checkout, PurchaseHistory, WishlistItem
from product.serializers import ProductSerializer
from product.models import Product

class ProfileSerializer(serializers.ModelSerializer):
    user = User
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'balance', 'contact_info', 'shopping_preferences']

    def create(self, validated_data):
        # Set the default balance to 0 when creating a new profile
        validated_data['balance'] = 0.00
        profile = super().create(validated_data)
        return profile


class DepositSerializer(serializers.ModelSerializer):
    user = User

    class Meta:
        model = Deposit
        fields = ['user', 'amount', 'created_at']


class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddToCart
        fields = ['id', 'user', 'product', 'quantity', 'added_at']


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ['id', 'user', 'total_amount', 'created_at']


class PurchaseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHistory
        fields = ('id', 'user', 'product', 'purchased_at')


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ['id', 'user', 'product', 'added_at']

