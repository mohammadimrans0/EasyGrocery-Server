from rest_framework import viewsets
from django.forms import ValidationError
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .models import AddToCart, Checkout, PurchaseHistory
from .serializers import AddToCartSerializer, CheckoutSerializer, PurchaseHistorySerializer
from user.models import Profile
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action

from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings


# Payment Initiation Function
def payment_int(user, total_amount, cart_items, product_name, product_category, checkout):
    try:
        # Fetch user profile details
        profile = Profile.objects.get(user=user)
        cus_name = profile.name
        cus_phone = profile.contact_info
    except ObjectDoesNotExist:
        raise ValidationError("Profile not found for the logged-in user.")

    # Use SSLCommerz to initiate payment
    sslcz = SSLCOMMERZ({
        'store_id': settings.SSLCOMMERZ["STORE_ID"],
        'store_pass': settings.SSLCOMMERZ["STORE_PASSWORD"],
        'issandbox': settings.SSLCOMMERZ["ISSANDBOX"]
    })

    post_body = {
        'total_amount': str(total_amount),
        'currency': settings.SSLCOMMERZ["CURRENCY"],
        'tran_id': f"TXN_{user.id}_{checkout.id}",
        # 'success_url': "http://127.0.0.1:8000/api/order/payment/success",
        # 'fail_url': "http://127.0.0.1:8000/api/order/payment/fail",
        # 'cancel_url': "http://127.0.0.1:8000/api/order/payment/cancel",
        'success_url': "https://easygrocery-server.onrender.com/api/order/payment/success/",
        'fail_url': "https://easygrocery-server.onrender.com/api/order/payment/fail/",
        'cancel_url': "https://easygrocery-server.onrender.com/api/order/payment/cancel/",
        'emi_option': 0,
        'cus_name': cus_name,
        'cus_email': user.email,
        'cus_phone': cus_phone,
        'product_name': product_name,
        'product_category': product_category,
        'cus_add1': "customer address",
        'cus_city': "Dhaka",
        'cus_country': "Bangladesh",
        'product_profile': "general",
        'shipping_method': "NO",
        'num_of_item': len(cart_items),
    }

    # Create the payment session
    response = sslcz.createSession(post_body)

    # Check if payment session was successfully created
    if 'GatewayPageURL' in response:
        return response['GatewayPageURL']
    else:
        return None


# Checkout Viewset
class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = request.user
        user = serializer.validated_data['user']
        total_amount = serializer.validated_data['total_amount']

        # Fetch the user's cart items
        cart_items = AddToCart.objects.filter(user=user)

        if not cart_items.exists():
            raise ValidationError("Your cart is empty. Please add items before checkout.")
        
        # Extract product details from cart items
        product_names = [item.product.name for item in cart_items]
        product_categories = [item.product.category for item in cart_items]

        # Set a default product name/category if multiple items exist
        product_name = product_names[0] if len(product_names) == 1 else "Multiple Products"
        product_category = product_categories[0] if len(product_categories) == 1 else "Mixed"

        # Save the checkout
        checkout = serializer.save(user=user)

        # Call the payment initiation function
        payment_url = payment_int(user, total_amount, cart_items, product_name, product_category, checkout)

        # Check if payment URL is returned
        if payment_url:
            # Add cart items to purchase history and clear the cart
            for item in cart_items:
                PurchaseHistory.objects.create(
                    user= user,
                    product= item.product,
                    purchased_at= timezone.now()
                )
                cart_items.delete()

            return Response({"payment_url": payment_url})
        else:
            return Response({"error": "Failed to initiate payment"}, status=400)
        

# Add to cart viewset
class AddToCartViewSet(viewsets.ModelViewSet):
    queryset = AddToCart.objects.all()
    serializer_class = AddToCartSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']


# Viewset for Purchase History
class PurchaseHistoryViewSet(viewsets.ModelViewSet):
    queryset = PurchaseHistory.objects.all()
    serializer_class = PurchaseHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']


@csrf_exempt
@action(detail=False, methods=['post'])
def payment_success(request):
    return redirect("https://easygrocery.vercel.app/payment/success")


@csrf_exempt
@action(detail=False, methods=['post'])
def payment_fail(request):
    return redirect("https://easygrocery.vercel.app/payment/fail")


@csrf_exempt
@action(detail=False, methods=['post'])
def payment_cancel(request):
    return redirect("https://easygrocery.vercel.app/payment/cancel")
