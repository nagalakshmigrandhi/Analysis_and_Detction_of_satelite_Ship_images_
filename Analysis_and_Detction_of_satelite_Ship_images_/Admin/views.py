from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from Users.models import User

def admin_check(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(admin_check, login_url='custom_admin:login')
def admin_home(request):
    users = User.objects.all()
    return render(request, 'admin/adminHome.html', {'users': users})

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, 'Welcome back, Admin!')
            return redirect('custom_admin:home')
        else:
            messages.error(request, 'Invalid admin credentials')
    return render(request, 'admin.html')

@user_passes_test(admin_check, login_url='custom_admin:login')
def view_users(request):
    users = User.objects.all()
    return render(request, 'admin/userDetails.html', {'users': users})

@user_passes_test(admin_check, login_url='custom_admin:login')
def activate_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.status = 'activated'
        user.save()
        messages.success(request, f'User {user.email} has been activated')
    except User.DoesNotExist:
        messages.error(request, 'User not found')
    return redirect('custom_admin:view_users')

@user_passes_test(admin_check, login_url='custom_admin:login')
def deactivate_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.status = 'deactivated'
        user.save()
        messages.success(request, f'User {user.email} has been deactivated')
    except User.DoesNotExist:
        messages.error(request, 'User not found')
    return redirect('custom_admin:view_users')

def admin_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out from admin panel')
    return redirect('custom_admin:login')