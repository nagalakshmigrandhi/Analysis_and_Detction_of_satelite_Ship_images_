from django.contrib import admin as django_admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('django-admin/', django_admin.site.urls, name='django_admin'),  # Django's built-in admin
    path('admin/', include(('Admin.urls', 'custom_admin'), namespace='custom_admin')),  # Our custom admin
    path('users/', include('Users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
