from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.contrib.auth import login, authenticate, logout

from .models import Profile, Deposit, AddToCart, Checkout, PurchaseHistory, WishlistItem
from .serializers import ResetPasswordSerializer, SignupSerializer, UserLoginSerializer, UserSerializer, ProfileSerializer, DepositSerializer, AddToCartSerializer, CheckoutSerializer, PurchaseHistorySerializer, WishlistItemSerializer
from django.contrib.auth.models import User

# user viewset
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

# profile viewset
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        if self.action in ['update', 'partial_update']:
            return Profile.objects.all()
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save()

# signup user
class SignupViewSet(viewsets.ViewSet):
    serializer_class = SignupSerializer

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login user
class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': "Invalid Username or Password"})
        return Response(serializer.errors)
    

# Logout user
class UserLogoutApiView(APIView):
    def post(self, request):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Logout successful."})


# reset password
class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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
        user = serializer.validated_data['user']  # The user is already the User object, not user_id
        total_amount = serializer.validated_data['total_amount']

        # Fetch the user's cart items
        cart_items = AddToCart.objects.filter(user=user)

        if not cart_items.exists():
            raise ValidationError("Your cart is empty. Please add items before checkout.")

        # Fetch the user's profile
        try:
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            raise ValidationError("Profile not found for the logged-in user.")

        # Deduct balance
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
            cart_items.delete()

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