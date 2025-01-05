from alipay import AliPay
from django.conf import settings
import os

def get_alipay():
    with open(settings.ALIPAY_APP_PRIVATE_KEY_PATH) as f:
        app_private_key_string = f.read()
    
    with open(settings.ALIPAY_ALIPAY_PUBLIC_KEY_PATH) as f:
        alipay_public_key_string = f.read()

    alipay = AliPay(
        appid=settings.ALIPAY_APPID,
        app_notify_url=settings.ALIPAY_NOTIFY_URL,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
        debug=settings.ALIPAY_DEBUG
    )
    return alipay

def create_alipay_order(order, payment):
    alipay = get_alipay()
    subject = f"订单号：{order.order_number}"
    
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=payment.id,
        total_amount=float(payment.amount),
        subject=subject,
        return_url=settings.ALIPAY_RETURN_URL,
        notify_url=settings.ALIPAY_NOTIFY_URL
    )
    
    if settings.ALIPAY_DEBUG:
        return f"https://openapi.alipaydev.com/gateway.do?{order_string}"
    return f"https://openapi.alipay.com/gateway.do?{order_string}" 