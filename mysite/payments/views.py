import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse

def sslcommerz_payment_initiate(request):
    post_data = {
        "store_id": settings.SSLCOMMERZ["STORE_ID"],
        "store_passwd": settings.SSLCOMMERZ["STORE_PASSWORD"],
        "total_amount": "100",  # Change dynamically
        "currency": settings.SSLCOMMERZ["CURRENCY"],
        "tran_id": "TXN_" + str(request.user.id) + "_1234",  # Unique transaction ID
        "success_url": settings.SSLCOMMERZ["SUCCESS_URL"],
        "fail_url": settings.SSLCOMMERZ["FAIL_URL"],
        "cancel_url": settings.SSLCOMMERZ["CANCEL_URL"],
        "emi_option": "0",
        "cus_name": request.user.get_full_name(),
        "cus_email": request.user.email,
        "cus_phone": "017XXXXXXXX",  # Provide user phone number
        "product_name": "Test Product",
        "product_category": "General",
        "product_profile": "general",
    }

    response = requests.post(settings.SSLCOMMERZ["INITIATE_URL"], data=post_data)
    response_data = response.json()

    if "GatewayPageURL" in response_data:
        return redirect(response_data["GatewayPageURL"])
    else:
        return JsonResponse({"error": "Failed to initiate payment"}, status=400)


def sslcommerz_payment_success(request):
    return JsonResponse({"message": "Payment successful", "data": request.GET})


def sslcommerz_payment_fail(request):
    return JsonResponse({"message": "Payment failed", "data": request.GET})


def sslcommerz_payment_cancel(request):
    return JsonResponse({"message": "Payment cancelled", "data": request.GET})
