from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Deposit, PurchaseHistory, Wishlist


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


class PurchaseHistorySerializer(serializers.ModelSerializer):
    user = User
    product = serializers.StringRelatedField()

    class Meta:
        model = PurchaseHistory
        fields = ['user', 'product', 'quantity', 'purchased_at']


class WishlistSerializer(serializers.ModelSerializer):
    user = User
    product = serializers.StringRelatedField()

    class Meta:
        model = Wishlist
        fields = ['user', 'product', 'added_at']
