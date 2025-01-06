from django.contrib import admin
from .models import Profile, Deposit, PurchaseHistory

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
    ordering = ('-created_at',)

@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'purchased_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('purchased_at',)

