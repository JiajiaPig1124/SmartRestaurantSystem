from django.db import models
from django.contrib.auth import get_user_model
from menu.models import Dish

User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = '购物车'

    def get_total_price(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name='购物车')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='菜品')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '购物车项'
        verbose_name_plural = '购物车项'
        unique_together = ('cart', 'dish')

    def get_subtotal(self):
        return self.dish.price * self.quantity

class Order(models.Model):
    ORDER_STATUS = (
        ('pending', '确认中'),
        ('confirmed', '已确认'),
        ('preparing', '制作中'),
        ('delivering', '配送中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )
    
    ORDER_TYPE = (
        ('dine_in', '堂食'),
        ('takeaway', '外卖'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    order_number = models.CharField(max_length=20, unique=True, verbose_name='订单号')
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE, verbose_name='订单类型')
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='pending', verbose_name='订单状态')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    notes = models.TextField(blank=True, verbose_name='备注')
    address = models.TextField(blank=True, verbose_name='配送地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']

    def __str__(self):
        return f'订单号：{self.order_number}'

    def generate_order_number(self):
        # 生成订单号：年月日时分秒+4位随机数
        from datetime import datetime
        import random
        now = datetime.now()
        return f"{now.strftime('%Y%m%d%H%M%S')}{random.randint(1000,9999)}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格') 

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('failed', '支付失败'),
        ('refunded', '已退款'),
    )
    
    PAYMENT_METHOD = (
        ('alipay', '支付宝'),
        ('wechat', '微信支付'),
    )
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', verbose_name='订单')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='支付金额')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD, verbose_name='支付方式')
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending', verbose_name='支付状态')
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name='交易号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    class Meta:
        verbose_name = '支付记录'
        verbose_name_plural = '支付记录'

    def __str__(self):
        return f'{self.order.order_number} - {self.get_payment_method_display()}' 

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1星'),
        (2, '2星'),
        (3, '3星'),
        (4, '4星'),
        (5, '5星'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review', verbose_name='订单')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_reviews', verbose_name='用户')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='评分')
    comment = models.TextField(verbose_name='评价内容')
    images = models.ManyToManyField('ReviewImage', blank=True, verbose_name='评价图片')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '订单评价'
        verbose_name_plural = '订单评价'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.order.order_number} - {self.get_rating_display()}'

class ReviewImage(models.Model):
    image = models.ImageField(upload_to='review_images/', verbose_name='图片')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        verbose_name = '评价图片'
        verbose_name_plural = '评价图片'

class ReviewReply(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='reply', verbose_name='评价')
    content = models.TextField(verbose_name='回复内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '评价回复'
        verbose_name_plural = '评价回复' 