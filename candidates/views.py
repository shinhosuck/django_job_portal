from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model 
from .forms import MessageForm, CandidateForm
from django.contrib import messages
from .models import Candidate
from employers.models import Job 


User = get_user_model()


def landing_page_view(request):
    if request.user.is_authenticated:
        return redirect('candidates:jobs')
    return render(request, 'landing_page.html')


def about_view(request):
    return render(request, 'about.html')


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


def candidate_register_view(request):
    form = CandidateForm(request.POST or None, request.FILES or None)
    context = {'form':form}
   
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            
    return render(request, 'candidates/candidate_register.html', context)


def candidates_view(request):
    candidates = Candidate.objects.all()

    context = {'candidates': candidates}

    return render(request, 'candidates/candidates.html', context)


def candidate_detail_view(request, slug):
    context = {}

    try:
        candidate = Candidate.objects.get(slug=slug)
    except Candidate.DoesNotExist:
        return redirect('candidates:candidates')
    
    context.update({'candidate': candidate})

    return render(request, 'candidates/candidate_detail.html', context)


def jobs_view(request):
    jobs = Job.objects.select_related('employer')
    
    context = {'jobs': jobs}

    return render(request, 'candidates/jobs.html', context)


def apply_to_a_job_view(request, slug):
    return redirect('employers:job-detail', slug=slug)