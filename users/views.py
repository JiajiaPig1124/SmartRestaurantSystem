from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserLoginForm, UserPreferenceForm
from .models import User, UserPreference
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages  # 添加消息框架

class IndexView(TemplateView):
    template_name = 'users/index.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # 创建用户偏好
        UserPreference.objects.create(
            user=self.object,
            taste='normal',
            spiciness=0
        )
        # 自动登录
        login(self.request, self.object)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST' and not context['form'].is_valid():
            context['show_modal'] = True
        return context

class LoginView(TemplateView):
    template_name = 'users/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserLoginForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # 获取 next 参数，如果没有则跳转到首页
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class ProfileView(UpdateView):
    model = User
    template_name = 'users/profile.html'
    fields = ['username', 'email', 'phone', 'avatar', 'address']
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user

def logout_view(request):
    logout(request)
    return redirect('home') 

@login_required
def profile_view(request):
    # 获取用户统计信息
    order_count = request.user.order_set.count()
    completed_orders = request.user.order_set.filter(status='completed').count()
    pending_orders = request.user.order_set.filter(status='pending').count()
    total_spent = sum(order.total_amount for order in request.user.order_set.filter(status='completed'))
    review_count = request.user.review_set.count()
    recent_orders = request.user.order_set.order_by('-created_at')[:5]

    context = {
        'order_count': order_count,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'total_spent': total_spent,
        'review_count': review_count,
        'recent_orders': recent_orders,
    }
    return render(request, 'users/profile.html', context)

@login_required
def update_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        request.user.avatar = request.FILES['avatar']
        request.user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.birthday = request.POST.get('birthday') or None
        user.address = request.POST.get('address')
        user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        
        if request.user.check_password(current_password):
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # 保持用户登录状态
            return JsonResponse({'status': 'success'})
        return JsonResponse({
            'status': 'error',
            'message': '当前密码不正确'
        })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def unbind_account(request):
    if request.method == 'POST':
        bind_type = request.POST.get('type')
        if bind_type == 'phone':
            request.user.phone = ''
            request.user.save()
            return JsonResponse({'status': 'success'})
        elif bind_type == 'wechat':
            # 实现微信解绑逻辑
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400) 