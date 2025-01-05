from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('menu/', include('menu.urls')),
    path('orders/', include('orders.urls')),
    path('merchant/', include('merchant.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 