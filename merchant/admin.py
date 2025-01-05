from django.contrib import admin
from .models import Merchant, BusinessHours, Announcement, Promotion, Review

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'phone', 'address', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'address', 'phone']

@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ['merchant', 'weekday', 'opening_time', 'closing_time', 'is_closed']
    list_filter = ['weekday', 'is_closed']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'merchant', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title', 'content']

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['title', 'merchant', 'promotion_type', 'is_active', 'start_time', 'end_time']
    list_filter = ['promotion_type', 'is_active']
    search_fields = ['title', 'description']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['merchant', 'user', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['comment'] 