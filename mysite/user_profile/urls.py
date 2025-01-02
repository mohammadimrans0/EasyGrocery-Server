from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, DepositViewSet, PurchaseHistoryViewSet, WishlistViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'deposits', DepositViewSet)
router.register(r'purchase-history', PurchaseHistoryViewSet)
router.register(r'wishlist', WishlistViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
