from django.shortcuts import render, redirect
from .models import Employer, Job
from .forms import EmployerForm, JobsForm
from django.contrib.auth.decorators import login_required


def employer_view(request):
    if request.user.is_authenticated:
        return redirect('employers:post-job')
    return render(request, 'employers/employers_landing_page.html')


# @login_required
def employer_register(request):
    form = EmployerForm(request.POST or None)
    context = {'form':form}

    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            return redirect('employers:post-job')

    return render(request, 'employers/employer_register.html', context)


# @login_required
def post_job_view(request):
    form = JobsForm(request.POST or None)
    context = {'form':form}
   
    # try:
    #     employer = Employer.objects.get(representative=request.user)
    # except Employer.DoesNotExist:
    #     employer = None 
    
    # if not employer:
    #     return redirect('employers:employer-register')
    
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)

    return render(request, 'employers/post_job.html', context)

