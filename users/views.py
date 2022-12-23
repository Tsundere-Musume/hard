from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import MyUser
from .forms import UserRegisterForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} created!')
        else:
            messages.error(request, 'Something went wrong.')
            return redirect('user-register')
        
        return redirect('user-signin')
    else:
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})
    
    