from django.urls import path
from .views import sslcommerz_payment_initiate, sslcommerz_payment_success, sslcommerz_payment_fail, sslcommerz_payment_cancel

urlpatterns = [
    path("initiate/", sslcommerz_payment_initiate, name="sslcommerz_initiate"),
    path("success/", sslcommerz_payment_success, name="sslcommerz_success"),
    path("fail/", sslcommerz_payment_fail, name="sslcommerz_fail"),
    path("cancel/", sslcommerz_payment_cancel, name="sslcommerz_cancel"),
]
