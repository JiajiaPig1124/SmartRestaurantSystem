from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.DishListView.as_view(), name='dish_list'),
    path('dish/<int:pk>/', views.DishDetailView.as_view(), name='dish_detail'),
    path('dish/add/', views.DishCreateView.as_view(), name='dish_create'),
    path('dish/<int:pk>/edit/', views.DishUpdateView.as_view(), name='dish_update'),
    path('dish/<int:pk>/delete/', views.DishDeleteView.as_view(), name='dish_delete'),
    path('dish/<int:pk>/stock/', views.update_stock, name='update_stock'),
] 