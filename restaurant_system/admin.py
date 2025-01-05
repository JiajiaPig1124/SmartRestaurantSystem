from django.contrib import admin
from django.db.models import Sum
from users.models import User
from orders.models import Order
from menu.models import Dish

class CustomAdminSite(admin.AdminSite):
    site_header = '智能餐饮管理系统'
    site_title = '智能餐饮管理系统'
    index_title = '管理控制台'

    def index(self, request, extra_context=None):
        # 统计数据
        extra_context = extra_context or {}
        extra_context['total_orders'] = Order.objects.count()
        extra_context['total_users'] = User.objects.count()
        extra_context['total_dishes'] = Dish.objects.filter(is_available=True).count()
        extra_context['total_revenue'] = Order.objects.filter(
            status='completed'
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # 为应用添加图标
        app_list = self.get_app_list(request)
        for app in app_list:
            if app['app_label'] == 'users':
                app['icon'] = 'fa-users'
            elif app['app_label'] == 'orders':
                app['icon'] = 'fa-shopping-cart'
            elif app['app_label'] == 'menu':
                app['icon'] = 'fa-utensils'
            elif app['app_label'] == 'merchant':
                app['icon'] = 'fa-store'
                
            # 为模型添加图标
            for model in app['models']:
                if 'User' in model['object_name']:
                    model['icon'] = 'fa-user'
                elif 'Order' in model['object_name']:
                    model['icon'] = 'fa-file-alt'
                elif 'Dish' in model['object_name']:
                    model['icon'] = 'fa-hamburger'
                elif 'Merchant' in model['object_name']:
                    model['icon'] = 'fa-store-alt'
                # 添加更多模型图标...

        extra_context['app_list'] = app_list
        return super().index(request, extra_context)

admin_site = CustomAdminSite() 