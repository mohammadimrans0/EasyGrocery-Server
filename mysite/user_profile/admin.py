from django.contrib import admin
from .models import Profile, Deposit, AddToCart, Checkout, PurchaseHistory, WishlistItem

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_info', 'shopping_preferences')
    search_fields = ('user__username', 'contact_info')
    list_filter = ('user__is_active',)

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)

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

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    list_filter = ('user', 'added_at')
    search_fields = ('user__username', 'product__name')

