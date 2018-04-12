from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='superadmin'),
    path('login/', views.acc_login, name='acc_login'),
    path('logout/', views.acc_logout, name='acc_logout'),
    path('<appname>/', views.app_form_list, name='app_form_list'),
    path('<appname>/<modelname>/', views.table_list, name='table_list'),
    path('<appname>/<modelname>/<int:obj_id>/change/', views.obj_change, name='obj_change'),
    path('<appname>/<modelname>/<int:obj_id>/delete/', views.obj_delete, name='obj_delete'),
    path('<appname>/<modelname>/add/', views.obj_add, name='obj_add'),
]
