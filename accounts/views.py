from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import (
    login, 
    authenticate, 
    logout
)
from .models import Profile
import os

def register_view(request):
    next = request.GET.get('next') or None

    if request.user.is_authenticated:
        messages.warning(request, "You are already registered and logged in!")
        return redirect('candidates:jobs')

    form = RegisterForm(request.POST or None)
    context = {
        'form':form,
        'next':next
    }

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            if instance:
                messages.success(request, 'Successfully registered!')
                if next:
                    return redirect(f'/login/?next={next}')
                return redirect('accounts:login')
            
    return render(request, 'accounts/register.html', context)


def login_view(request):    
    next = request.GET.get('next') or None
    form = LoginForm(request.POST or None)
    context = {'form': form}

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            user = authenticate(
                request, 
                username=data['username'], 
                password=data['password']
            )

            if user:
                login(request, user)
                if next:
                    return redirect(next)
                messages.success(request, 'Successfully logged in!')
                return redirect('candidates:jobs')
            
        context['error'] = 'Username or password did not match.'

    return render(request, 'accounts/login.html', context)
            

def logout_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "You haven't logged in yet!")
        return redirect('candidates:jobs')

    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Successfully logged out!')
        return redirect('candidates:landing-page')
    return render(request, 'accounts/logout.html')


def user_profile_view(request):
    return render(request, 'accounts/profile.html')