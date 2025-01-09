from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import NotAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from django.db import transaction

from .models import Profile, Deposit, AddToCart, Checkout, PurchaseHistory, WishlistItem
from .serializers import ProfileSerializer, DepositSerializer, AddToCartSerializer, CheckoutSerializer, PurchaseHistorySerializer, WishlistItemSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from product.models import Product


# Viewset for Profile
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def by_user_id(self, request, user_id=None):
        try:
            profile = Profile.objects.get(user__id=user_id)
        except Profile.DoesNotExist:
            raise NotFound(detail="Profile not found for the given user ID")
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


# Viewset for Deposit money
class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer

    def perform_create(self, serializer):
        # using transaction to ensure atomicity
        with transaction.atomic():
            deposit = serializer.save()

            profile = Profile.objects.get(user=deposit.user)
            profile.balance += deposit.amount
            profile.save()

            return Response({
                'message': 'Deposit successful',
                'balance': profile.balance
            }, status=status.HTTP_201_CREATED)


# add to cart
class AddToCartViewSet(viewsets.ModelViewSet):
    queryset = AddToCart.objects.all()
    serializer_class = AddToCartSerializer

    def get_queryset(self):
        user = self.request.user

        # Check if a user_id is passed in the query parameters
        user_id = self.request.query_params.get("user_id")

        if user_id:
            # Allow access to another user's cart only if the logged-in user has special permissions
            if user.is_authenticated and (user.is_staff or user.is_superuser):
                return AddToCart.objects.filter(user_id=user_id)
            else:
                raise PermissionDenied("You do not have permission to view this user's cart.")

        # Default behavior: return the logged-in user's cart
        if user.is_authenticated:
            return AddToCart.objects.filter(user_id=user.id)
        else:
            raise NotAuthenticated("You must be logged in to view this data.")

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated("You must be logged in to add items to the cart.")

        product_data = self.request.data.get("product")
        if not product_data or not isinstance(product_data, dict):
            raise serializers.ValidationError("Invalid product data.")

        product_id = product_data.get("id")
        if not product_id:
            raise serializers.ValidationError("Product ID is required.")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")

        # Create the cart item with quantity set to 1
        serializer.save(user=user, product=product, quantity=1)



# viewset for Checkout
class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

    def perform_create(self, serializer):
        user = serializer.validated_data['user']
        total_amount = serializer.validated_data['total_amount']

        # Calculate total amount from the cart
        cart_items = AddToCart.objects.filter(user=user)
        calculated_total = sum(item.product.price * item.quantity for item in cart_items)  # Assuming product.price exists

        if calculated_total != total_amount:
            raise ValidationError("The total amount provided does not match the calculated total.")

        # Deduct balance
        profile = user.profile
        if profile.balance >= calculated_total:
            profile.balance -= calculated_total
            profile.save()

            # Save the checkout
            checkout_instance = serializer.save()

            # Create purchase history and clear cart
            for item in cart_items:
                PurchaseHistory.objects.create(
                    user=user,
                    product=item.product,
                    purchased_at=now()
                )
            cart_items.delete()

        else:
            raise ValidationError("Insufficient balance for checkout.")


# Viewset for Purchase History
class PurchaseHistoryViewSet(viewsets.ModelViewSet):
    queryset = PurchaseHistory.objects.all()
    serializer_class = PurchaseHistorySerializer

# viewset for wishlist
class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer

    def get_queryset(self):
        user = self.request.user

        # Ensure the user is authenticated
        if not user.is_authenticated:
            raise NotAuthenticated("You must be logged in to view this data.")

        # Check if a user_id is passed in the query parameters
        user_id = self.request.query_params.get("user_id")

        if user_id:
            # Allow access to other users' wishlist only if the logged-in user has special permissions (e.g., is_staff)
            if user.is_staff or user.is_superuser:
                return WishlistItem.objects.filter(user_id=user_id)  # Filter by user_id in query parameters
            else:
                raise PermissionDenied("You do not have permission to view this user's wishlist.")

        # Default behavior: return the logged-in user's wishlist
        return WishlistItem.objects.filter(user_id=user.id)



