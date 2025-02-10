from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddToCartViewSet, CheckoutViewSet, PurchaseHistoryViewSet, sslcommerz_payment_success, sslcommerz_payment_fail, sslcommerz_payment_cancel

router = DefaultRouter()
router.register(r'cart', AddToCartViewSet, basename='add_to_cart')
router.register(r'checkout', CheckoutViewSet, basename='checkout')
router.register(r'purchase-history', PurchaseHistoryViewSet, basename='purchase_history')


urlpatterns = [
    path('', include(router.urls)),
    path("payment/success/", sslcommerz_payment_success, name="sslcommerz_success"),
    path("payment/fail/", sslcommerz_payment_fail, name="sslcommerz_fail"),
    path("payment/cancel/", sslcommerz_payment_cancel, name="sslcommerz_cancel"),
]