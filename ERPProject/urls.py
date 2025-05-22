from django.urls import path, include
from django.contrib import admin
from login import views, urls

urlpatterns = [
    path('admin/login/', views.get_user),
    path('admin/', admin.site.urls),
    path('', views.get_user),
    path('login/', views.get_user),
    path('sales/', include('sales.urls', namespace="sales")),
    path('hr/', include('hr.urls', namespace="hr")),
    path('finance/', include('finance.urls', namespace="finance")),
]
