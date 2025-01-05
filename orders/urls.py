from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/pay/', views.pay_order, name='pay_order'),
    path('alipay/notify/', views.alipay_notify, name='alipay_notify'),
    path('alipay/return/', views.alipay_return, name='alipay_return'),
    path('payment/<int:payment_id>/success/', views.payment_success, name='payment_success'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
    path('order/<int:order_id>/review/', views.create_review, name='create_review'),
    path('reviews/', views.review_list, name='review_list'),
    path('review/<int:review_id>/', views.review_detail, name='review_detail'),
    path('review/<int:review_id>/reply/', views.reply_review, name='reply_review'),
    path('orders/', views.order_list, name='order_list'),
] 