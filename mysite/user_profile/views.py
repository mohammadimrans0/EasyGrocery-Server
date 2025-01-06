from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db import transaction

from .models import Profile, Deposit, AddToCart, Checkout, PurchaseHistory, WishlistItem
from .serializers import ProfileSerializer, DepositSerializer, AddToCartSerializer, CheckoutSerializer, PurchaseHistorySerializer, WishlistItemSerializer
from django.contrib.auth.models import User

# Viewset for Profile
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

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
        return AddToCart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product_id = self.request.data.get("product_id")
        quantity = self.request.data.get("quantity", 1)

        # Get the product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")

        # Check if the item already exists in the cart, update the quantity if it does
        cart_item, created = AddToCart.objects.get_or_create(user=self.request.user, product=product)
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        # Serialize the updated cart item
        serializer = AddToCartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def cart_items(self, request):
        cart_items = self.get_queryset()
        serializer = AddToCartSerializer(cart_items, many=True)
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


class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer

    def get_queryset(self):
        # Filter wishlist items by the authenticated user
        user = self.request.user
        return WishlistItem.objects.filter(user=user)


