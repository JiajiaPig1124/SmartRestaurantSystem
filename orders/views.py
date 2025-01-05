from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem, Order, OrderItem, Payment, Review, ReviewImage, ReviewReply
from menu.models import Dish
from django.db import transaction
import random
import string
from .utils import create_alipay_order
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ReviewForm, ReviewReplyForm

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'orders/cart_detail.html', {'cart': cart})

@login_required
@require_POST
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if not dish.is_available or dish.stock <= 0:
        messages.error(request, '该菜品暂时无法购买')
        return redirect('menu:dish_detail', pk=dish_id)
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity > dish.stock:
        messages.error(request, '购买数量超过库存')
        return redirect('menu:dish_detail', pk=dish_id)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        dish=dish,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > dish.stock:
            messages.error(request, '购买数量超过库存')
            return redirect('menu:dish_detail', pk=dish_id)
        cart_item.save()
    
    messages.success(request, f'{dish.name} 已添加到购物车')
    return redirect('orders:cart_detail')

@login_required
@require_POST
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 0))
    
    if quantity > 0:
        if quantity > cart_item.dish.stock:
            return JsonResponse({
                'status': 'error',
                'message': '购买数量超过库存'
            })
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    cart = cart_item.cart
    return JsonResponse({
        'status': 'success',
        'subtotal': cart_item.get_subtotal() if quantity > 0 else 0,
        'total': cart.get_total_price(),
        'total_items': cart.get_total_items()
    })

@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, f'{cart_item.dish.name} 已从购物车移除')
    return redirect('orders:cart_detail')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.error(request, '购物车为空')
        return redirect('orders:cart_detail')

    if request.method == 'POST':
        order_type = request.POST.get('order_type')
        notes = request.POST.get('notes', '')

        try:
            with transaction.atomic():
                # 创建订单
                order = Order.objects.create(
                    user=request.user,
                    order_number=Order().generate_order_number(),
                    order_type=order_type,
                    total_amount=cart.get_total_price(),
                    notes=notes,
                    address=request.user.address if order_type == 'takeaway' else ''
                )

                # 创建订单项
                for cart_item in cart.items.all():
                    if cart_item.quantity > cart_item.dish.stock:
                        raise ValueError(f'{cart_item.dish.name}库存不足')
                    
                    # 创建订单项
                    OrderItem.objects.create(
                        order=order,
                        dish=cart_item.dish,
                        quantity=cart_item.quantity,
                        price=cart_item.dish.price
                    )
                    
                    # 更新库存
                    cart_item.dish.stock -= cart_item.quantity
                    cart_item.dish.sales_count += cart_item.quantity
                    cart_item.dish.save()

                # 清空购物车
                cart.items.all().delete()

                messages.success(request, f'订单创建成功！订单号：{order.order_number}')
                return redirect('orders:order_detail', order_id=order.id)

        except ValueError as e:
            messages.error(request, str(e))
            return redirect('orders:cart_detail')
        except Exception as e:
            messages.error(request, '订单创建失败，请重试')
            return redirect('orders:cart_detail')

    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'pending':
        messages.error(request, '该订单状态不允许支付')
        return redirect('orders:order_detail', order_id=order.id)
    
    # 创建支付记录
    payment = Payment.objects.create(
        order=order,
        amount=order.total_amount,
        payment_method='alipay'
    )
    
    # 生成支付链接
    pay_url = create_alipay_order(order, payment)
    return redirect(pay_url)

@csrf_exempt
def alipay_notify(request):
    """支付宝异步通知"""
    data = request.POST.dict()
    signature = data.pop("sign")
    
    alipay = get_alipay()
    success = alipay.verify(data, signature)
    
    if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        payment = Payment.objects.get(id=data["out_trade_no"])
        payment.status = 'paid'
        payment.transaction_id = data["trade_no"]
        payment.paid_at = timezone.now()
        payment.save()
        
        order = payment.order
        order.status = 'confirmed'
        order.save()
        
        return HttpResponse("success")
    return HttpResponse("fail")

def alipay_return(request):
    """支付宝同步通知"""
    data = request.GET.dict()
    signature = data.pop("sign")
    
    alipay = get_alipay()
    success = alipay.verify(data, signature)
    
    if success:
        payment = Payment.objects.get(id=data["out_trade_no"])
        return redirect('orders:payment_success', payment_id=payment.id)
    return redirect('orders:payment_failed')

@login_required
def create_review(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'completed':
        messages.error(request, '只能评价已完成的订单')
        return redirect('orders:order_detail', order_id=order.id)
    
    if hasattr(order, 'review'):
        messages.error(request, '该订单已评价')
        return redirect('orders:order_detail', order_id=order.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.user = request.user
            review.save()
            
            # 处理图片上传
            images = request.FILES.getlist('images')
            for image in images:
                review_image = ReviewImage.objects.create(image=image)
                review.images.add(review_image)
            
            messages.success(request, '评价提交成功！')
            return redirect('orders:order_detail', order_id=order.id)
    else:
        form = ReviewForm()
    
    return render(request, 'orders/review_form.html', {
        'form': form,
        'order': order
    })

@login_required
def review_list(request):
    reviews = Review.objects.filter(user=request.user).select_related('order')
    return render(request, 'orders/review_list.html', {'reviews': reviews})

@staff_member_required
def reply_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.method == 'POST':
        form = ReviewReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.review = review
            reply.save()
            messages.success(request, '回复成功！')
            return redirect('orders:review_detail', review_id=review.id)
    else:
        form = ReviewReplyForm()
    
    return render(request, 'orders/reply_form.html', {
        'form': form,
        'review': review
    })

def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    return render(request, 'orders/review_detail.html', {'review': review})

@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, order__user=request.user)
    return render(request, 'orders/payment_success.html', {
        'payment': payment,
        'order': payment.order
    })

@login_required
def payment_failed(request):
    messages.error(request, '支付失败，请重试')
    return redirect('orders:cart_detail')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {
        'orders': orders
    }) 