from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'}))
    mobile = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Enter your mobile number'}))
    locality = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your locality'}))
    state = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter your state'}))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )

    class Meta:
        model = User
        fields = ('email', 'name', 'mobile', 'locality', 'state', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if len(mobile) < 10 or not mobile.isdigit():
            raise forms.ValidationError('Please enter a valid 10-digit mobile number.')
        return mobile

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.mobile = self.cleaned_data['mobile']
        user.locality = self.cleaned_data['locality']
        user.state = self.cleaned_data['state']
        user.status = 'activated'
        
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter your password'})

    def clean_username(self):
        return self.cleaned_data.get('username')
