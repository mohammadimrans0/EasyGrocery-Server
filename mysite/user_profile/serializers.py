from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Deposit, PurchaseHistory
from product.serializers import ProductSerializer
from product.models import Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
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


class PurchaseHistorySerializer(serializers.ModelSerializer):
    user = User
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = PurchaseHistory
        fields = ['user', 'product_name', 'quantity', 'purchased_at']

