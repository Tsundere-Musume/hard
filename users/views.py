from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import MyUser
from .forms import UserRegisterForm, UserSigninForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} created!')
        else:
            messages.error(request, 'Invalid Form.')
            return redirect('user-register')
        
        return redirect('user-signin')
    else:
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})
    
def signin(request):
    if request.method == 'POST':
        form = UserSigninForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            passwd = form.cleaned_data.get('password')
            user = authenticate(request, username=uname, password=passwd)
            if user:
                login(request, user)
                messages.success(request, 'Log-in Successful')

                # Go somewhere after login
                return redirect('# Go Somewhere')

            else:
                messages.error(request, 'Invalid Credentials')
        else:
            messages.error('Invalid Form')
        return redirect('user-signin')
    else:
        form = UserSigninForm()
        return render(request, 'users/signin.html', {'form': form})
