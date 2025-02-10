from django.contrib import admin
from .models import AddToCart, Checkout, PurchaseHistory

# Register your models here.
@admin.register(AddToCart)
class AddToCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    search_fields = ('user__username', 'product__name')


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount') 
    search_fields = ('user__username',)  

@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'purchased_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('purchased_at',)