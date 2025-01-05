from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Merchant(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, verbose_name='关联用户')
    name = models.CharField(max_length=100, verbose_name='商家名称')
    description = models.TextField(blank=True, verbose_name='商家描述')
    address = models.CharField(max_length=200, verbose_name='地址')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    logo = models.ImageField(upload_to='merchant/logos/', blank=True, verbose_name='商家logo')
    business_license = models.ImageField(upload_to='merchant/licenses/', verbose_name='营业执照')
    is_active = models.BooleanField(default=True, verbose_name='是否营业')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '商家信息'
        verbose_name_plural = '商家信息'

    def __str__(self):
        return self.name

class BusinessHours(models.Model):
    WEEKDAY_CHOICES = (
        (0, '周一'),
        (1, '周二'),
        (2, '周三'),
        (3, '周四'),
        (4, '周五'),
        (5, '周六'),
        (6, '周日'),
    )
    
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='business_hours', verbose_name='商家')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, verbose_name='星期')
    opening_time = models.TimeField(verbose_name='开始营业时间')
    closing_time = models.TimeField(verbose_name='结束营业时间')
    is_closed = models.BooleanField(default=False, verbose_name='是否休息')

    class Meta:
        verbose_name = '营业时间'
        verbose_name_plural = '营业时间'
        unique_together = ('merchant', 'weekday')
        ordering = ['weekday']

    def __str__(self):
        return f'{self.merchant.name} - {self.get_weekday_display()}'

class Announcement(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='announcements', verbose_name='商家')
    title = models.CharField(max_length=100, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')
    is_active = models.BooleanField(default=True, verbose_name='是否显示')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '商家公告'
        verbose_name_plural = '商家公告'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Promotion(models.Model):
    PROMOTION_TYPE = (
        ('discount', '折扣'),
        ('reduction', '满减'),
        ('gift', '赠品'),
    )
    
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='promotions', verbose_name='商家')
    title = models.CharField(max_length=100, verbose_name='活动标题')
    description = models.TextField(verbose_name='活动描述')
    promotion_type = models.CharField(
        max_length=20, 
        choices=PROMOTION_TYPE, 
        default='discount',
        verbose_name='活动类型'
    )
    discount_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                       validators=[MinValueValidator(0), MaxValueValidator(1)],
                                       verbose_name='折扣值')
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                       verbose_name='最低消费金额')
    reduction_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         verbose_name='优惠金额')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '优惠活动'
        verbose_name_plural = '优惠活动'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time

class Review(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='merchant_reviews', verbose_name='用户')
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name='评分')
    comment = models.TextField(verbose_name='评价内容')
    created_at = models.DateTimeField(auto_now_add=True) 