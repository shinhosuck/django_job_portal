from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout


def register_view(request):
    form = RegisterForm(request.POST or None)
    context = {'form':form}

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            if instance:
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
                return redirect('jobs:home')
            
        context['error'] = 'Username or password did not match.'

    return render(request, 'accounts/login.html', context)
            
                