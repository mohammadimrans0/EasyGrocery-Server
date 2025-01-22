from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Deposit, AddToCart, Checkout, PurchaseHistory, WishlistItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'balance', 'contact_info', 'shopping_preferences']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user, created = User.objects.get_or_create(**user_data)
        validated_data['user'] = user
        validated_data['balance'] = 0.00
        profile = super().create(validated_data)
        return profile

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['user', 'amount', 'created_at']

class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddToCart
        fields = ['id', 'user', 'product', 'product_name', 'product_price', 'quantity', 'added_at']

class CheckoutSerializer(serializers.ModelSerializer):
    serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
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