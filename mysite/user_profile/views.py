from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Profile, Deposit, AddToCart, Checkout, PurchaseHistory, WishlistItem
from .serializers import ProfileSerializer, DepositSerializer, AddToCartSerializer, CheckoutSerializer, PurchaseHistorySerializer, WishlistItemSerializer
from django.utils.timezone import now
from product.models import Product

# Viewset for Profile
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']


# viewset for Checkout
class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

    def perform_create(self, serializer):
        user = self.request.user
        total_amount = serializer.validated_data['total_amount']

        # Fetch the user's cart items
        cart_items = AddToCart.objects.filter(user=user)

        if not cart_items.exists():
            raise ValidationError("Your cart is empty. Please add items before checkout.")

        # Deduct balance
        profile = user.profile
        if profile.balance >= total_amount:
            profile.balance -= total_amount
            profile.save()

            # Save the checkout
            checkout_instance = serializer.save(user=user)

            # Add cart items to purchase history and clear the cart
            for item in cart_items:
                PurchaseHistory.objects.create(
                    user=user,
                    product=item.product,
                    purchased_at=now()
                )
            cart_items.delete()  # Clear the cart

        else:
            raise ValidationError("Insufficient balance for checkout.")



# Viewset for Purchase History
class PurchaseHistoryViewSet(viewsets.ModelViewSet):
    queryset = PurchaseHistory.objects.all()
    serializer_class = PurchaseHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']


# viewset for wishlist
class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']