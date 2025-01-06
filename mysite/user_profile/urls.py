from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, DepositViewSet, PurchaseHistoryViewSet

router = DefaultRouter()
router.register(r'profile', ProfileViewSet)
router.register(r'deposit', DepositViewSet)
router.register(r'purchase-history', PurchaseHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
