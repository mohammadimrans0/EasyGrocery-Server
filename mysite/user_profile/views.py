from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Profile, Deposit, PurchaseHistory
from .serializers import ProfileSerializer, DepositSerializer, PurchaseHistorySerializer
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


# Viewset for Purchase History
class PurchaseHistoryViewSet(viewsets.ModelViewSet):
    queryset = PurchaseHistory.objects.all()
    serializer_class = PurchaseHistorySerializer

