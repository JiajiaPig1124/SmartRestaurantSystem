from django.urls import path
from .views import DashboardView

urlpatterns = [
    path('admin/', DashboardView.as_view(), name='admin_dashboard'),
    # ... 其他 URL 配置
] 