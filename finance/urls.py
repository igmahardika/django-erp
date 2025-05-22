from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    # path('outcome/', views.outcome, name='outcome'),
    # path('logout/', views.logout_view, name='logout')
]
