from django.shortcuts import render, redirect
from .models import Employer, Job
from .forms import EmployerForm, JobsForm
from django.contrib import messages
from utils.decorators import user_login_required


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
    form = JobsForm(request.POST or None)
    context = {'form':form}

    employers = request.user.employer_set.all()
    
    if not employers.exists():
        messages.error(request, 'Please register your company first to post a job.')
        return redirect('employers:employer-register')
    else:
        context['employers'] = employers

    if request.method == 'POST':
        employer_name = request.POST.get('employers')

        try:
            employer = employers.get(company=employer_name)
        except Exception as e:
            messages.error(request, "Employer does not exists.")

        if employer:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.company = employer
                instance.save()
                messages.success(request, 'New job posted successfully.')
                return redirect('employers:employer-dashboard')
            else:
                messages.error(request, 'There was an unknown error. Please try again')

    return render(request, 'employers/post_job.html', context)


@user_login_required
def employer_dashboard_view(request):
    employers = request.user.employer_set.all()
    context = {'employers':employers}

    return render(request, 'employers/employer_dashboard.html', context)


def employer_detail_view(request, slug):
    context = {}

    try:
        employer = Employer.objects.get(slug=slug)
    except Employer.DoesNotExist:
        messages.error(request, 'Employer does not exit. Please try again.')
        return redirect('employers:employer-detail', slug=slug)
    
    if employer:
        jobs = employer.job_set.all()
        context.update({'employer':employer, 'jobs':jobs})

    return render(request, 'employers/employer_detail.html', context)


def employer_job_detail(request, slug):
    employer_slug = request.GET.get('employer') or None
    redirect_url = request.META['HTTP_REFERER']

    try:
        employer = Employer.objects.get(slug=employer_slug)
    except Employer.DoesNotExist:
        employer = None

    try:
        job = Job.objects.get(slug=slug)
    except Job.DoesNotExist:
        return redirect('employers:employer-detail', slug=employer_slug)
    
    context = {'redirect_url': redirect_url, 'job': job}
    
    return render(request, 'employers/job_detail.html', context)