from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm
from .models import User, PredictionHistory
from .dataProcesing import prediction_image
import os
from django.conf import settings
from django.utils import timezone

@login_required
def user_home(request):
    # Get statistics
    user_predictions = PredictionHistory.objects.filter(user=request.user)
    total_predictions = user_predictions.count()
    total_ships = sum(entry.num_ships for entry in user_predictions)
    
    # Calculate accuracy rate (for demonstration, using a fixed value)
    accuracy_rate = 95  # This should be calculated based on actual model performance
    
    return render(request, 'users/userHome.html', {
        'total_predictions': total_predictions,
        'total_ships': total_ships,
        'accuracy_rate': accuracy_rate
    })

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('users:prediction')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('users:prediction')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('login')

@login_required
def prediction(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        
        # Save uploaded image
        upload_dir = 'static/uploads'
        os.makedirs(upload_dir, exist_ok=True)
        image_path = os.path.join(upload_dir, image.name)
        
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        # Process image
        result = prediction_image(image_path)
        
        if result['success']:
            # Save to history
            history_entry = PredictionHistory(
                user=request.user,
                input_image=image,
                output_image=result['output_path'],
                num_ships=result['num_ships']
            )
            history_entry.save()
            
            context.update({
                'output_image': '/' + result['output_path'].replace('\\', '/'),
                'input_image': '/' + image_path.replace('\\', '/'),
                'num_ships': result['num_ships'],
                'success': True,
                'message': result['message']
            })
        else:
            context.update({
                'success': False,
                'message': result['message']
            })
            messages.error(request, result['message'])
    
    return render(request, 'users/prediction.html', context)

@login_required
def history(request):
    # Get the user's prediction history
    history_entries = PredictionHistory.objects.filter(user=request.user)
    
    return render(request, 'users/history.html', {
        'history': history_entries,
        'MEDIA_URL': settings.MEDIA_URL
    })
