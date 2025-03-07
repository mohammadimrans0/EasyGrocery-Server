from rest_framework import serializers
from .models import AddToCart, Checkout, PurchaseHistory
from django.contrib.auth.models import User

class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddToCart
        fields = ['id', 'user', 'product', 'quantity', 'added_at']

class CheckoutSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Checkout
        fields = ['id', 'user', 'total_amount']
        

class PurchaseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHistory
        fields = ('id', 'user', 'product', 'purchased_at')