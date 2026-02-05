from django.urls import path
from . import views

app_name = 'admin'  # This sets the URL namespace

urlpatterns = [
    path('', views.admin_home, name='home'),
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('users/', views.view_users, name='view_users'),
    path('users/activate/<int:user_id>/', views.activate_user, name='activate_user'),
    path('users/deactivate/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
]
