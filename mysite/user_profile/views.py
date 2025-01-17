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
from django.utils.timezone import now
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

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def by_user_id(self, request, user_id=None):
        cartItem = AddToCart.objects.filter(user__id=user_id)
        
        if not cartItem.exists():
            raise NotFound(detail="You don't have any items in the cart.")
        
        serializer = self.get_serializer(cartItem, many=True)
        return Response(serializer.data)


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

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def by_user_id(self, request, user_id):
        wishlist = WishlistItem.objects.filter(user__id=user_id)
        if not wishlist.exists():
            raise NotFound(detail=f"No wishlist items found for user ID {user_id}.")

        serializer = self.get_serializer(wishlist, many=True)
        return Response(serializer.data)