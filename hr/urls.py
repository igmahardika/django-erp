from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    path('', views.index, name='index'),
    path('jobs/', views.jobs, name='jobs'),
    path('job/<int:job_id>/', views.job, name='job'),
    path('applicants/', views.applicants, name='applicants'),
    path('applicant/<int:app_id>/', views.applicant, name='applicant'),
    path('employees/', views.employees, name='employees'),
    path('employee/<int:emp_id>/', views.employee, name='employee'),
    path('logout/', views.logout_user, name='logout'),
    path('update_job/<int:job_id>/', views.update_job, name='update_job')
]
