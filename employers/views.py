from django.shortcuts import render, redirect
from .models import Employer, Job
from .forms import EmployerForm, JobForm
from django.contrib import messages
from utils.decorators import user_login_required
from django.http import Http404


def employer_landing_page_view(request):
    return render(request, 'employers/employers_landing_page.html')


@user_login_required
def employer_register(request):
    form = EmployerForm(request.POST or None, request.FILES or None)
    context = {'form':form}

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.representative = request.user
            instance.save()

            return redirect('employers:post-job')

    return render(request, 'employers/employer_register.html', context)


@user_login_required
def post_job_view(request):
    user = request.user
    form = JobForm(request.POST or None)
    context = {'form':form}

    employers = request.user.employers.all()
    
    if not employers.exists():
        messages.error(request, 'Please register your company first to post a job.')
        return redirect('employers:employer-register')
    else:
        context['employers'] = employers

    if request.method == 'POST':
        employer_name = request.POST.get('employer')

        try:
            employer = employers.get(employer_name=employer_name)
        except Exception as e:
            messages.error(request, "Employer does not exists.")
            return render(request, 'employers/employer_post_job.html', context)
        
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employer = employer
            instance.save()
            messages.success(request, 'New job posted successfully.')
            return redirect('employers:employer-dashboard')
        
    return render(request, 'employers/employer_post_job.html', context)


@user_login_required
def employer_dashboard_view(request):
    
    if request.user.profile.user_type == 'job seeker':
        messages.warning(request, 'You do not have employer account.')
        return redirect('candidates:jobs')


    employers = request.user.employers \
        .prefetch_related('jobs')
    context = {'employers':employers}

    return render(request, 'employers/employer_dashboard.html', context)


def employer_detail_view(request, slug):
    redirect_url = request.GET.get('redirect')
    context = {}

    try:
        employer = Employer.objects.get(slug=slug)
    except Employer.DoesNotExist:
        messages.error(request, 'Employer does not exit. Please try again.')
        return redirect('employers:employer-detail', slug=slug)
    
    if employer:
        jobs = employer.jobs.all()
        context.update(
            {
                'employer':employer, 
                'jobs':jobs,
                'redirect_url':redirect_url
            }
        )

    return render(request, 'employers/employer_detail.html', context)


def employer_job_detail(request, slug):
    redirect_url = request.GET.get('redirect') or None
    user = request.user

    context = {
        'redirect_url': redirect_url, 
        'applied': False
    }

    if not redirect_url:
        raise Http404('Page Does Not Exist.')
    
    try:
        job = Job.objects.get(slug=slug)
    except Job.DoesNotExist:
        messages.error(request, 'Job does not exist.')
        return redirect(redirect_url)
    
    context.update({'job': job})

    if user.is_authenticated and job.applicants.filter(user=user):
        context.update({'applied': True})

    return render(request, 'employers/employer_job_detail.html', context)


def employer_job_update_view(request, slug):
    user = request.user
    context = {}

    try:
        job = Job.objects.get(slug=slug, employer__representative=user)
    except Job.DoesNotExist:
        messages.error(request, 'Job does not exist')
        return redirect('employers:employer-dashboard')
    
    form = JobForm(request.POST or None, instance=job)

    context.update(
            {
                'form':form, 
                'job':job,
                'employer':job.employer.employer_name
            }
        )
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()

    return render(request, 'employers/employer_job_update.html', context)