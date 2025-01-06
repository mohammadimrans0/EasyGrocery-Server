from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, DepositViewSet, AddToCartViewSet, CheckoutViewSet, PurchaseHistoryViewSet, WishlistItemViewSet

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'deposit', DepositViewSet, basename='deposit')
router.register(r'cart', AddToCartViewSet, basename='add_to_cart')
router.register(r'checkout', CheckoutViewSet, basename='checkout')
router.register(r'purchase-history', PurchaseHistoryViewSet, basename='purchase_history')
router.register(r'wishlist', WishlistItemViewSet, basename='wishlist')


urlpatterns = [
    path('', include(router.urls)),
]
