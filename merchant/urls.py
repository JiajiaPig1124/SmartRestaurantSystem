from django.urls import path
from . import views

app_name = 'merchant'

urlpatterns = [
    path('', views.merchant_list, name='merchant_list'),
    path('<int:merchant_id>/', views.merchant_detail, name='merchant_detail'),
    path('<int:merchant_id>/review/', views.merchant_review, name='merchant_review'),
] 