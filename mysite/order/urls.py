from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddToCartViewSet, CheckoutViewSet, PurchaseHistoryViewSet, payment_success, payment_fail, payment_cancel

router = DefaultRouter()
router.register(r'cart', AddToCartViewSet, basename='add_to_cart')
router.register(r'checkout', CheckoutViewSet, basename='checkout')
router.register(r'purchase-history', PurchaseHistoryViewSet, basename='purchase_history')


urlpatterns = [
    path('', include(router.urls)),
    path("payment/success", payment_success, name="payment_success"),
    path("payment/fail", payment_fail, name="payment_fail"),
    path("payment/cancel", payment_cancel, name="payment_cancel"),
]