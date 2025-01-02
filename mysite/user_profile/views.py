from rest_framework import viewsets
from .models import Profile, Deposit, PurchaseHistory, Wishlist
from .serializers import ProfileSerializer, DepositSerializer, PurchaseHistorySerializer, WishlistSerializer
from django.contrib.auth.models import User

# Viewset for Profile
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# viewset for deposit money
class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer


# Viewset for Purchase History
class PurchaseHistoryViewSet(viewsets.ModelViewSet):
    queryset = PurchaseHistory.objects.all()
    serializer_class = PurchaseHistorySerializer

# Viewset for Wishlist
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
