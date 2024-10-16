from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model 
from .forms import MessageForm, CandidateForm
from django.contrib import messages
from .models import Candidate

User = get_user_model()


def landing_page_view(request):
    if request.user.is_authenticated:
        return redirect('candidates:jobs')
    return render(request, 'landing_page.html')


def jobs_view(request):
    return render(request, 'candidates/jobs.html')


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
            return redirect('candidates:home')

        context['error'] = 'There was an error. Please try again.'
    return render(request, 'contact.html', context)


def about_view(request):
    return render(request, 'about.html')


def candidate_register_view(request):
    form = CandidateForm(request.POST or None, request.FILES or None)
    context = {'form':form}
   
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            
    return render(request, 'candidates/candidate_register.html', context)