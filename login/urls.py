from django.urls import path
from django.contrib import admin
from login import views

urlpatterns = [
    path('', views.get_user),
    path('login', views.get_user),
    # path('login/error', views.login_error)
]
