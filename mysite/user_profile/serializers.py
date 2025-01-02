from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Deposit, PurchaseHistory, Wishlist


class ProfileSerializer(serializers.ModelSerializer):
    user = User

    class Meta:
        model = Profile
        fields = ['user', 'image', 'contact_info', 'shopping_preferences']


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
