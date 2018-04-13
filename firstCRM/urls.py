from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='sales_dashboard'),
    path('stu_enrollment/', views.stu_enrollment, name='stu_enrollment'),
    path('stu_enrollment/<int:enrollment_id>', views.enrollment_agree, name='enrollment_agree'),
]
