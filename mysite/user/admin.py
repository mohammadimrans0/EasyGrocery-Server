from django.contrib import admin
from .models import Profile, WishlistItem

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_info', 'shopping_preferences')
    search_fields = ('user__username', 'contact_info')
    list_filter = ('user__is_active',)

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    list_filter = ('user', 'added_at')
    search_fields = ('user__username', 'product__name')

