from django.contrib import admin
from .models import ShopDetails

@admin.register(ShopDetails)
class ShopDetailsAdmin(admin.ModelAdmin):
    list_display = ('user','shop_name', 'owner_name', 'city', 'state', 'pincode', 'contact_number', 'gstin', 'details_filled')
    list_filter = ('state', 'city', 'details_filled')
    search_fields = ('shop_name', 'owner_name', 'city', 'pincode', 'gstin', 'contact_number')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'shop_name', 'owner_name', 'contact_number', 'gstin')
        }),
        ('Address', {
            'fields': ('area', 'city', 'state', 'pincode')
        }),
        ('Shop Timings', {
            'fields': ('start_time', 'end_time')
        }),
        ('Status', {
            'fields': ('details_filled',)
        }),
    )
