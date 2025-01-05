from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
import json

@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admin/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 获取基础统计数据
        context['total_orders'] = Order.objects.count()
        context['total_users'] = User.objects.count()
        context['total_revenue'] = Order.objects.aggregate(
            total=Sum('total_amount'))['total'] or 0
        
        # 计算趋势
        context['order_trend'] = self.calculate_trend('orders')
        context['user_trend'] = self.calculate_trend('users')
        context['revenue_trend'] = self.calculate_trend('revenue')
        
        # 计算趋势的绝对值
        context['order_trend_abs'] = abs(context['order_trend'])
        context['user_trend_abs'] = abs(context['user_trend'])
        context['revenue_trend_abs'] = abs(context['revenue_trend'])
        
        # 图表数据
        context['order_chart'] = self.get_trend_chart_options('orders')
        context['user_chart'] = self.get_trend_chart_options('users')
        context['revenue_chart'] = self.get_trend_chart_options('revenue')
        context['sales_chart'] = self.get_sales_chart_options()
        
        # 热销菜品排行
        context['top_dishes'] = self.get_top_dishes()
        
        return context

    def calculate_trend(self, metric_type):
        # 计算同比增长率
        now = timezone.now()
        current_period = self.get_metric_value(metric_type, now - timedelta(days=7), now)
        prev_period = self.get_metric_value(metric_type, now - timedelta(days=14), now - timedelta(days=7))
        
        if prev_period == 0:
            return 0
        return ((current_period - prev_period) / prev_period) * 100

    def get_metric_value(self, metric_type, start_date, end_date):
        if metric_type == 'orders':
            return Order.objects.filter(created_at__range=(start_date, end_date)).count()
        elif metric_type == 'users':
            return User.objects.filter(date_joined__range=(start_date, end_date)).count()
        elif metric_type == 'revenue':
            result = Order.objects.filter(created_at__range=(start_date, end_date)).aggregate(
                total=Sum('total_amount'))['total']
            return result or 0

    def get_trend_chart_options(self, metric_type):
        # 生成迷你图表配置
        data = self.get_trend_data(metric_type)
        return {
            'grid': {'left': 0, 'right': 0, 'top': 0, 'bottom': 0},
            'xAxis': {'show': False, 'type': 'category'},
            'yAxis': {'show': False, 'type': 'value'},
            'series': [{
                'type': 'line',
                'smooth': True,
                'showSymbol': False,
                'data': data,
                'areaStyle': {'opacity': 0.2},
                'lineStyle': {'width': 2},
                'itemStyle': {'color': '#1a73e8'},
            }]
        }

    def get_sales_chart_options(self):
        # 生成销售趋势图表配置
        return {
            'tooltip': {'trigger': 'axis'},
            'grid': {'left': '3%', 'right': '4%', 'bottom': '3%', 'containLabel': True},
            'xAxis': {
                'type': 'category',
                'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            },
            'yAxis': {'type': 'value'},
            'series': [{
                'name': '销售额',
                'type': 'line',
                'smooth': True,
                'data': [150, 230, 224, 218, 135, 147, 260]
            }]
        }

    def get_top_dishes(self):
        # 获取热销菜品数据
        return Dish.objects.annotate(
            sales_count=Count('orderitem'),
            revenue=Sum('orderitem__subtotal')
        ).order_by('-sales_count')[:10] 

    def get_trend_data(self, metric_type):
        # 获取过去7天的数据
        now = timezone.now()
        data = []
        for i in range(7):
            start_date = now - timedelta(days=i+1)
            end_date = now - timedelta(days=i)
            value = self.get_metric_value(metric_type, start_date, end_date)
            data.append(value)
        return list(reversed(data))  # 反转数据以按时间顺序显示 