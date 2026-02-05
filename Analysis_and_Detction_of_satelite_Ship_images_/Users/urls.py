from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.user_home, name='home'),
    path('prediction/', views.prediction, name='prediction'),
    path('history/', views.history, name='history'),
    path('logout/', views.user_logout, name='logout'),
]
