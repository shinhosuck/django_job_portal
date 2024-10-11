from django.shortcuts import render, redirect
from accounts.models import Profile
from django.contrib.auth import get_user_model 
from django.contrib.auth.decorators import login_required
from .forms import MessageForm
from django.contrib import messages

User = get_user_model()


def landing_page_view(request):
    if request.user.is_authenticated:
        return redirect('jobs:jobs')
    return render(request, 'jobs/landing_page.html')


def jobs_view(request):
    context = {
        'message': 'Jobs page'
    }
    return render(request, 'jobs/jobs.html', context)


def contact_view(request):
    form = MessageForm(request.POST or None)
    context = {'form':form}

    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            
            try:
                user = User.objects.get(email=message.email)
            except User.DoesNotExist:
                user = None 
            if user:
                message.user = user

            message.save()

            messages.success(request, 'Message successfully submited.')
            return redirect('jobs:home')

        context['error'] = 'There was an error. Please try again.'
    return render(request, 'jobs/contact.html', context)


def about_view(request):
    return render(request, 'jobs/about.html')