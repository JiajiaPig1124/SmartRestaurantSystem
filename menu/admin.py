from django.contrib import admin
from .models import Cuisine, Dish

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'merchant', 'cuisine', 'price', 'stock', 'sales_count', 'is_available']
    list_filter = ['merchant', 'cuisine', 'is_available']
    search_fields = ['name', 'merchant__name']
    readonly_fields = ['sales_count', 'created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('merchant', 'cuisine', 'name', 'description', 'price')
        }),
        ('库存信息', {
            'fields': ('stock', 'is_available')
        }),
        ('图片', {
            'fields': ('image',)
        }),
        ('统计信息', {
            'fields': ('sales_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    ) 