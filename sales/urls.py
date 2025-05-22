from django.urls import path
from django.urls import reverse_lazy
from sales import views
from django.views.generic.base import RedirectView

app_name = 'sales'

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/', views.clients, name='clients'),
    path('products/', views.products, name='products'),
    path('specifics/<int:product_id>/', views.detail, name='product_detail'),
    path('logout/', views.logout_view, name='logout')


    # url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^specifics/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='product_detail'),
]
