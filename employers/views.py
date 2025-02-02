from django.shortcuts import render, redirect
from .models import Employer, Job
from .forms import EmployerForm, JobForm
from django.contrib import messages
from utils.decorators import user_login_required
from django.http import Http404
from accounts.models import Profile
from accounts.forms import ProfileUpdateForm
from django.urls import reverse


def employer_landing_page_view(request):
    user = request.user 

    if user.is_authenticated:
        user_type = user.profile.user_type
        if user_type == 'job seeker':
            return redirect('candidates:landing-page')
    return render(request, 'employers/employers_landing_page.html')


@user_login_required
def employer_register(request):
    form = EmployerForm(request.POST or None, request.FILES or None)
    context = {'form':form}
    user = request.user

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            instance.profile = user.profile
            instance.save()
            return redirect('employers:post-job')
                
    return render(request, 'employers/employer_register.html', context)


@user_login_required
def post_job_view(request):
    user = request.user
    form = JobForm(request.POST or None)
    context = {'form':form}

    employers = user.profile.employers.all()

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
            return redirect('employers:employer-profile')
        
    return render(request, 'employers/employer_post_job.html', context)


@user_login_required
def employer_profile_view(request):
    data_type = request.GET.get('data_type')
    user = request.user

    if request.user.profile.user_type == 'job seeker':
        messages.warning(request, 'You do not have employer account.')
        return redirect('candidates:jobs')

    employers = user.profile.employers \
        .prefetch_related('jobs')
    
    context = {
        'profile': user.profile,
        'employers':employers,
        'data_type': data_type,
        'social_link': user.profile.social_link and \
            user.profile.social_link.split('//')[1],
        'portfolio_or_personal_website': user.profile.portfolio_or_personal_website and \
            user.profile.portfolio_or_personal_website('//')[1],
    }

    return render(request, 'employers/employer_profile.html', context)


def employer_detail_view(request, slug):

    redirect_url = request.GET.get('redirect')
    user = request.user
    context = {}

    # if not redirect_url:
    #     raise Http404('Page Does Not Exist.')

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
                'redirect_url':redirect_url,
                'employer_profile_user': employer.profile.user
            }
        )
    
    return render(request, 'employers/employer_detail.html', context)


def employer_job_detail(request, slug):
    redirect_url = request.GET.get('redirect')
    user = request.user

    context = {
        'redirect_url': redirect_url, 
        'applied': False,
        'is_owner': False
    }

    # if not redirect_url:
    #     raise Http404('Page Does Not Exist.')
    
    try:
        job = Job.objects.get(slug=slug)
    except Job.DoesNotExist:
        messages.error(request, 'Job does not exist.')
        return redirect(redirect_url)
    
    context['job'] = job

    if user == job.employer.profile.user:
        context['is_owner'] = True

    if user.is_authenticated and user.profile.user_type == 'job seeker':
        if job.applicants.filter(profile__user=user):
            context['applied'] = True

    return render(request, 'employers/employer_job_detail.html', context)


@user_login_required
def employer_update_view(request, slug):
    data_type = request.GET.get('data_type')
    instance = None
    form = None

    if data_type == 'profile':
        try:
            instance = Profile.objects.get(slug=slug)
        except Profile.DoesNotExist:
            instance = None
    elif data_type == 'employer':
        try:
            instance = Employer.objects.get(slug=slug)
        except Employer.DoesNotExist:
            instance = None 
    
    if data_type == 'profile':
        form = ProfileUpdateForm(
            request.POST or None, 
            request.FILES or None,
            instance=instance
        )
    elif data_type == 'employer':
        form = EmployerForm(
            request.POST or None, 
            request.FILES or None,
            instance=instance
        )
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            query_param = f'?data_type={data_type}'
            url = f"{reverse('employers:employer-profile')}{query_param}"
            return redirect(url)
    
    context = {
        'instance': instance,
        'data_type': data_type,
        'form': form
    }

    return render(request, 'employers/employer_update.html', context)


@user_login_required
def employer_job_update_view(request, slug):
    user = request.user
    context = {}

    try:
        job = Job.objects.get(slug=slug, employer__profile__user=user)
    except Job.DoesNotExist:
        messages.error(request, 'Job does not exist')
        return redirect('employers:employer')
    
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
            return redirect('employers:employer-profile')
    return render(request, 'employers/employer_job_update.html', context)