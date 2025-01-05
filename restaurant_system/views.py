from django.shortcuts import render
from merchant.models import Merchant, Promotion

def home(request):
    popular_merchants = Merchant.objects.filter(is_active=True)[:3]
    latest_promotions = Promotion.objects.filter(is_active=True).order_by('-created_at')[:3]
    
    return render(request, 'index.html', {
        'popular_merchants': popular_merchants,
        'latest_promotions': latest_promotions,
    }) 