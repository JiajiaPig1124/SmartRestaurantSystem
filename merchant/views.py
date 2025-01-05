from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Merchant, Announcement, Promotion

def merchant_detail(request, merchant_id):
    merchant = get_object_or_404(Merchant, id=merchant_id, is_active=True)
    announcements = merchant.announcements.filter(is_active=True)
    promotions = merchant.promotions.filter(
        is_active=True,
        start_time__lte=timezone.now(),
        end_time__gte=timezone.now()
    )
    business_hours = merchant.business_hours.all()
    
    return render(request, 'merchant/merchant_detail.html', {
        'merchant': merchant,
        'announcements': announcements,
        'promotions': promotions,
        'business_hours': business_hours,
    })

def merchant_list(request):
    merchants = Merchant.objects.filter(is_active=True)
    return render(request, 'merchant/merchant_list.html', {
        'merchants': merchants
    })

@login_required
def merchant_review(request, merchant_id):
    merchant = get_object_or_404(Merchant, id=merchant_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.create(
            merchant=merchant,
            user=request.user,
            rating=rating,
            comment=comment
        )
        
        messages.success(request, '评价提交成功！')
        return redirect('merchant:merchant_detail', merchant_id=merchant.id)
    
    return render(request, 'merchant/review_form.html', {
        'merchant': merchant
    }) 