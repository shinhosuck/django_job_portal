from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import (
    RegisterForm, 
    LoginForm, 
    ProfileUpdateForm
)
from django.contrib import messages
from django.contrib.auth import (
    login, 
    authenticate, 
    logout
)
from .models import Profile
from utils.decorators import user_login_required

def register_view(request):
    next = request.GET.get('next') or None

    if request.user.is_authenticated:
        messages.warning(request, "You are already registered and logged in!")
        return redirect('candidates:jobs')

    form = RegisterForm(request.POST or None)

    context = {
        'form':form,
    }

    if request.method == 'POST':
        if form.is_valid():
            form.save()
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
                messages.success(request, 'Successfully logged in!')

                if next:
                    return redirect(next)
                else:
                    if user.profile.user_type:
                        return redirect('accounts:profile')
                    else:
                        path = reverse('accounts:profile-update')
                        redir_url = f'{path}?message=Candidate profile is not set yet. Please complete the following forms.'
                        return redirect(redir_url)
            else:
                messages.error(request, 'Username or password did not match.')

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


@user_login_required
def profile_update_form_view(request):
    user = request.user
    message = request.GET.get('message')

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        messages.error(request, 'There was a unknown server error. Please try again.')
        return redirect('candidates:jobs')

    form = ProfileUpdateForm(
        request.POST or None, 
        request.FILES or None, 
        instance=profile
    )
    
    if request.method == 'POST':
        if form.is_valid():
            profile_form = form.save()

            user_type = profile_form.user_type
            
            if user_type == 'job seeker':
                return redirect('candidates:candidate-register')
            else:
                return redirect('employers:employer-register')

    context = {
            'form': form,
            'message': message or None
        }

    return render(request, 'accounts/profile_update_form.html', context)


@user_login_required
def profile_view(request):
    profile = request.user.profile
    context = {
        'profile': profile
    }
    return render(request, 'accounts/profile.html', context)