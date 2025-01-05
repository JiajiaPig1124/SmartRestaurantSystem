from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Cuisine, Dish
from .forms import CuisineForm, DishForm

class DishListView(ListView):
    model = Dish
    template_name = 'menu/dish_list.html'
    context_object_name = 'dishes'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset()
        cuisine = self.request.GET.get('cuisine')
        if cuisine:
            queryset = queryset.filter(cuisine_id=cuisine)
        return queryset.filter(is_available=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cuisines'] = Cuisine.objects.all()
        return context

class DishDetailView(DetailView):
    model = Dish
    template_name = 'menu/dish_detail.html'
    context_object_name = 'dish'

@method_decorator(staff_member_required, name='dispatch')
class DishCreateView(CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'menu/dish_form.html'
    success_url = reverse_lazy('menu:dish_list')
    
    def form_valid(self, form):
        messages.success(self.request, '菜品创建成功！')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class DishUpdateView(UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'menu/dish_form.html'
    success_url = reverse_lazy('menu:dish_list')
    
    def form_valid(self, form):
        messages.success(self.request, '菜品更新成功！')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class DishDeleteView(DeleteView):
    model = Dish
    template_name = 'menu/dish_confirm_delete.html'
    success_url = reverse_lazy('menu:dish_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '菜品删除成功！')
        return super().delete(request, *args, **kwargs)

@staff_member_required
def update_stock(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        new_stock = request.POST.get('stock')
        if new_stock and new_stock.isdigit():
            dish.stock = int(new_stock)
            dish.save()
            messages.success(request, f'{dish.name}库存更新成功！')
    return redirect('menu:dish_list') 