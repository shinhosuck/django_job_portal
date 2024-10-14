from django.shortcuts import render, redirect
from .models import Employer, Job
from .forms import EmployerForm, JobsForm
from django.contrib import messages
from django.urls import reverse


def employer_view(request):
    # if request.user.is_authenticated:
    #     return redirect('employers:employer-dashboard')
    return render(request, 'employers/employers_landing_page.html')


def employer_register(request):
    form = EmployerForm(request.POST or None)
    context = {'form':form}

    # if not request.user.is_authenticated:
    #     messages.error(request, 'Please log in to preceed to requested page.')
    #     return redirect('/login/?next=/employers/register/')

    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            return redirect('employers:post-job')

    return render(request, 'employers/employer_register.html', context)


def post_job_view(request):
    form = JobsForm(request.POST or None)
    context = {'form':form}

    # if not request.user.is_authenticated:
    #     messages.error(request, 'Please log in to preceed to requested page.')
    #     return redirect('/login/?next=/post/job/')
   
    # try:
    #     employer = Employer.objects.get(representative=request.user)
    # except Employer.DoesNotExist:
    #     employer = None 
    
    # if not employer:
    #     messages.error(request, 'Please register your company first to post a job.')
    #     return redirect('employers:employer-register')
    
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)

    return render(request, 'employers/post_job.html', context)


def employer_dashboard_view(request):
    return render(request, 'employers/employer_dashboard.html')