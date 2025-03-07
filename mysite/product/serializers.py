from rest_framework import serializers
from .models import Product, ProductReview


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'description', 'price', 'stock', 'category', 'product_owner']


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'user', 'rating', 'review', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
