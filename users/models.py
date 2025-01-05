from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    wechat_bound = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        
    def __str__(self):
        return self.username

class UserPreference(models.Model):
    TASTE_CHOICES = [
        ('light', '清淡'),
        ('normal', '普通'),
        ('spicy', '重口味'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taste = models.CharField(max_length=20, choices=TASTE_CHOICES, verbose_name='口味偏好')
    spiciness = models.IntegerField(choices=[(i, i) for i in range(6)], verbose_name='辣度偏好')  # 0-5级辣度
    
    class Meta:
        verbose_name = '用户偏好'
        verbose_name_plural = '用户偏好' 