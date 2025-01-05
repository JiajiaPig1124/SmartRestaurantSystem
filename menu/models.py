from django.db import models
from merchant.models import Merchant

class Cuisine(models.Model):
    name = models.CharField(max_length=100, verbose_name='菜系名称')
    description = models.TextField(blank=True, verbose_name='描述')

    class Meta:
        verbose_name = '菜系'
        verbose_name_plural = '菜系'

    def __str__(self):
        return self.name

class Dish(models.Model):
    merchant = models.ForeignKey(
        Merchant, 
        on_delete=models.CASCADE, 
        related_name='dishes', 
        verbose_name='所属商家',
        null=True,
        blank=True
    )
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True, verbose_name='菜系')
    name = models.CharField(max_length=100, verbose_name='菜品名称')
    description = models.TextField(blank=True, verbose_name='描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    image = models.ImageField(upload_to='dishes/', blank=True, verbose_name='图片')
    is_available = models.BooleanField(default=True, verbose_name='是否可用')
    stock = models.IntegerField(default=0, verbose_name='库存')
    sales_count = models.IntegerField(default=0, verbose_name='销量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '菜品'
        verbose_name_plural = '菜品'
        ordering = ['-sales_count']

    def __str__(self):
        return f'{self.merchant.name} - {self.name}' 