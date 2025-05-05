from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model 
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from employers.models import Job, Employer
from accounts.models import Profile, AppliedJob, SavedJob
from django.urls import reverse
from accounts.forms import ProfileUpdateForm
from .forms import (
    MessageForm,
    CandidateQualificationForm,
    EducationForm,
    ExperienceForm
)
from .models import (
    CandidateQualification,
    Education,
    Experience
)
from datetime import datetime
from textwrap import dedent
import json

# HELPER FUNCTIONS FROM UTILS DIR
from utils.handle_filter_jobs import (
    get_filter_jobs,
    filter_jobs_by_user_location,
    search_filter_job,
    convert_queryset_to_json_data
)
from utils.decorators import user_login_required
from utils.geo_location import get_user_ip
from utils.generate_suggestions import generate_suggestions
from utils.create_candiate_profile import (
    create_or_update_qualification, 
    create_or_update_education,
    create_or_update_experience,
    fetch_previous_form_data,
    prefetch_form_data
)

# django social login
from social_django.models import UserSocialAuth


User = get_user_model()


def landing_page_view(request):
    user = request.user
    
    if user.is_authenticated:
        if user.profile.user_type == 'employer':
            return redirect('employers:employer')
        else:
            return redirect('candidates:jobs')
        
    return render(request, 'candidates/candidates_landing_page.html')


def fetch_user_location_view(request):
    '''
    Handles a request to fetch the user's 
    location based on their IP address.

    - Initial request originates from "candidates.js",
        "getUserIP()" function.
    - Uses "get_user_ip()" helper to extract the user's IP.
    - Returns a JSON response containing the user's 
        location (country, city, state).
    '''
    location = get_user_ip(request)

    return JsonResponse(location, status=200)


def get_search_form_suggestions(request):

    """
    - This function get triggered on intial render.
    - This function get triggere when the user enters 
        some value in the search inputs.
    - Not when search button is clicked.
    - AJAX call comes from candiates_search_suggestions.js.
    - async function getSuggestions()
    """

    # User queries
    search = request.GET.get('search')
    searched_location = request.GET.get('location')

    # Data from user ip
    location =  get_user_ip(request)
    country_code = location.get('country_code')
    country = location.get('country')
    state_or_province = location.get('state')
    user_city = location.get('city')

    # Populate queryset using user location
    queryset = Job.objects.filter(Q(employer__country__iexact=country_code) |
        Q(employer__city__iexact=user_city)|Q(employer__state_or_province__iexact=state_or_province)) \
        .values('job_title','industry','job_type','employer__city','employer__state_or_province')
    
    """ 
    Queryset will be available on initial render and on every AJAX request.
    Populate queryset with user:
    - country_code or
    - state_or_province or
    - user_city 
    """

    # if queryset is unavailable, this block will be run.
    if not queryset and search or searched_location:
        if search:
            queryset = Job.objects.filter(Q(employer__employer_name__icontains=search)|
                Q(industry__icontains=search)|Q(job_title__icontains=search)|
                Q(job_type__icontains=search)|Q(work_location__icontains=search)) \
                .values('job_title','industry','job_type')
            
        if searched_location:
            queryset = Job.objects.filter(Q(employer__city__icontains=searched_location)|
                Q(employer__state_or_province__icontains=searched_location)) \
                .values('employer__city', 'employer__state_or_province')

    """
    - This block will be run after initial render.
    - It will only run if the queryset is not available.
    - It will be triggered only when uer inputs search values
    - Queryset will be populated based on user search input.
    """

    context = generate_suggestions(queryset, search, searched_location)

    return JsonResponse(
            {**context,'search':search, 
             'searched_location':searched_location, 'city':user_city,
             'state_or_province':state_or_province
            }, 
            status=200
        )
   

def job_search_view(request):
    content_type = request.headers.get('Content-Type')
    search_query = request.GET.get('search')
    search_location = request.GET.get('location')
    user_location = get_user_ip(request)
    context = {
        'jobs': None
    }
 
    if not search_query or not search_location:
        context['message'] = '''
        Sorry! Your search did not return anything.
        Make sure that Keyword or location field aren\'t empty.
        '''
        return render(request, 'candidates/candidates_search_results.html', context)

    if search_query and search_location:
        jobs, message = search_filter_job(search_query, search_location, user_location)
        context['jobs'] = jobs 
        context['message'] = message
    
    if content_type == 'application/json':
        if context['jobs']:
            json_context = convert_queryset_to_json_data(context)
            if json_context:
                return JsonResponse(json_context)
        return JsonResponse({'message': 'no jobs available'})

    return render(request, 'candidates/candidates_search_results.html', context)



@user_login_required
def candidate_add_career_detail_view(request):
    scroll_to = request.GET.get('scroll_to')
    data_type = request.GET.get('type')
    user = request.user
    data = request.POST

    try:
        resume = user.profile.candidatequalification.get_resume_url()
    except CandidateQualification.DoesNotExist:
        resume = None

    if not user.profile.user_type:
        message = '?message=Please complete your profile.'
        return redirect(f"{reverse('accounts:profile-update')}{message}")
    
    if request.method == 'POST':
        if data_type == 'qualification':
            resume = request.FILES.get('resume')
            context = create_or_update_qualification(
                data, 
                resume, 
                user, 
                data_type
            )
            return JsonResponse(context)
    
        if data_type == 'education':
            context = create_or_update_education(
                data,
                user, 
                data_type
            )
            return JsonResponse(context)
        
        if data_type == 'experience':
            context = create_or_update_experience(
                data, 
                user, 
                data_type
            )
            return JsonResponse(context)
        
    context = {
        'resume': resume or '',
        'scroll_to': scroll_to or ''
    }
    
    return render(request, 'candidates/candidates_add_career_detail.html', context)


def get_form_data_view(request):
    data = json.loads(request.body.decode('utf-8'))
    
    qualification = data.get('qualification')
    education = data.get('education')
    experience = data.get('experience')

    context = fetch_previous_form_data(qualification, education, experience)
    return JsonResponse(context)


def prefetch_form_data_view(request):
    user = request.user

    if user.is_authenticated:
        context = prefetch_form_data(user)
        return JsonResponse(context)
    
    context = {
        'error':'You must login first.'
    }
    return JsonResponse(context)


def candidates_view(request):
    candidates = CandidateQualification.objects.all()

    context = {'candidates': candidates}
    return render(request, 'candidates/candidates.html', context)


def candidate_detail_view(request, slug):
    context = {}

    try:
        candidate = CandidateQualification.objects.get(slug=slug)
    except CandidateQualification.DoesNotExist:
        return redirect('candidates:candidates')
    
    context.update({'candidate': candidate})

    return render(request, 'candidates/candidates_detail.html', context)


def jobs_view(request):
    jobs = Job.objects.select_related('employer')
    pagination = request.GET.get('jobPaginate')
    suggested_jobs = request.GET.get('q')

    # Get user location
    location_data = get_user_ip(request)
    country_code = location_data and location_data.get('country_code')
    state = location_data and location_data.get('state')
    city = location_data and location_data.get('city')

    qualification = None
    user = request.user
    context = {
        'jobs_exist': True
    }

    increment = 3
    start = 0 
    end = 6

    if request.user.is_authenticated:
        try:
            qualification = user.profile.candidatequalification
        except CandidateQualification.DoesNotExist:
            qualification = None

    qs, message = filter_jobs_by_user_location(country_code, state, city,
            jobs, qualification)
     
    context['jobs'] = qs
    context ['message'] = message

    if pagination:
        start = int(pagination) 
        end = start + increment

    # Checks jobs next set of qs exists.
    if not context['jobs'][end:end+increment]:
        context['jobs_exist'] = False

    context['jobs'] = context['jobs'][start:end]
    context['paginate'] = {'job_paginate': end}
    context['location'] = json.dumps(location_data)
    context['q_param'] = suggested_jobs
    
    # One of the jobs page dashboard link button
    if suggested_jobs:
        context['jobs'] = get_filter_jobs(context['jobs'])
        return JsonResponse(context)

    if pagination:
        context['jobs'] = get_filter_jobs(context['jobs'])
        return JsonResponse(context)
     
    return render(request, 'candidates/candidates_jobs.html', context)


def job_detail_view(request, slug):
    user = request.user
    redirect_url = request.GET.get('redirect')
    context = {
        'redirect_url': redirect_url
    }

    try:
        job = Job.objects.get(slug=slug)
    except Job.DoesNotExist:
        job = None
    
    context['job'] = job

    if user.is_authenticated and user.profile:
        try:
            qualification = CandidateQualification.objects.get(profile = user.profile)
        except CandidateQualification.DoesNotExist:
            qualification = None

        if qualification:
            user_type = user.profile.user_type
            if user_type == 'job seeker':
                if qualification in context['job'].applicants.all():
                    context['applied'] = True
                if SavedJob.objects.filter(saved_job=job, profile=user.profile):
                    context['job_saved'] = True
        # print('JOB SAVED:', SavedJob.objects.filter(saved_job=context['job'], profile=user.profile))
    return render(request, 'candidates/candidates_job_detail.html', context)


def filter_jobs_page_dashboard_view(request):
    user = request.user
    q_param= request.GET.get('q')
    context = {
        'jobs_exist': True
    }
    jobs = None

    applied_job_pagination = request.GET.get('appliedJobPaginate')
    saved_job_pagination = request.GET.get('savedJobPaginate')

    increment = 3
    start = 0
    end = 6

    if user.is_authenticated:
        if q_param == 'applied_jobs':
            jobs = [job.applied_job for job in user.profile.applied_jobs.all()]
        elif q_param == 'saved_jobs':
            jobs = [job.saved_job for job in user.profile.saved_jobs.all()]

    if q_param == 'applied_jobs':
        context['paginate'] = {'applied_job_paginate': end}
    elif q_param == 'saved_jobs':
        context['paginate'] = {'saved_job_paginate': end}
    
    if applied_job_pagination:
        start = int(applied_job_pagination)
        end = start + increment
        context['paginate'] = {'applied_job_paginate': end}
    if saved_job_pagination:
        start = int(saved_job_pagination)
        end = start + increment
        context['paginate'] = {'saved_job_paginate': end}

    if jobs:
        job_list = get_filter_jobs(jobs[start:end])
        context['jobs'] = job_list
    else:
        context['jobs'] = 'No jobs'
    
    if not context['jobs'][end:end+increment]:
        context['jobs_exist'] = False 

    context['q_param'] = q_param

    return JsonResponse(context)


@user_login_required
def apply_to_a_job_view(request, slug):
    user = request.user
    
    try:
        job = Job.objects.get(slug=slug)
    except Job.DoesNotExist:
        messages.error(request, 'Job does not exist. Pleas try again.')
        return redirect('candidates:jobs')
    
    try:
        candidate = CandidateQualification.objects.get(profile=user.profile)
    except CandidateQualification.DoesNotExist:
        messages.error(request, 'You must create your profile first.')
        return redirect('candidates:candidate-register')
    
    job.applicants.add(candidate)
    instance, created = AppliedJob.objects.get_or_create(profile=user.profile, applied_job=job)

    reverse_url = reverse('candidates:candidate-job-detail', kwargs={'slug': slug})
    url = f'{reverse_url}?redirect=/candidates/jobs/'

    messages.success(request, f'Successfully applied to {job.job_title}.')
    return redirect(url)


@user_login_required
def save_job_view(request, slug):
    user = request.user 

    try:
        job = Job.objects.get(slug=slug)
    except Job.DoesNotExist:
        job = None 

    instance, created = SavedJob.objects.get_or_create(profile=user.profile, saved_job=job)
 
    reverse_url = reverse('candidates:candidate-job-detail', kwargs={'slug': slug})
    url = f'{reverse_url}?redirect=/candidates/jobs/'

    messages.success(request, f'Job {job.job_title} successfully saved.')
    return redirect(url)


@user_login_required
def update_candidate_profile_info_view(request, slug):
    data_type = request.GET.get('data_type')
    form = None
    context = {}
    profile = request.user.profile

    print('DATA TYPE:', data_type)

    if not data_type:
        return redirect('accounts:profile')

    if data_type == 'profile':
        form = ProfileUpdateForm(
                request.POST or None, 
                request.FILES or None, 
                instance=Profile.objects.get(slug=slug)
            )
    elif data_type == 'qualification':
        form = CandidateQualificationForm(
                request.POST or None, 
                request.FILES or None, 
                instance=CandidateQualification.objects.get(slug=slug)
            )
    elif data_type == 'education':
        form = EducationForm(
                request.POST or None, 
                request.FILES or None, 
                instance=Education.objects.get(slug=slug)
            )
    elif data_type == 'experience':
        form = ExperienceForm(
                request.POST or None, 
                request.FILES or None, 
                instance=Experience.objects.get(slug=slug)
            )
        
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            redirect_url = f"{request.GET.get('redirect_url')}?data_type={data_type}"
            return redirect(redirect_url)
        else:
            print(form.errors)

    context['form'] = form
    context['data_type'] = data_type
    context['slug'] = slug
    context['redirect_url'] = reverse('accounts:profile')

    return render(
            request, 
            'candidates/candidates_update_career_profile_form.html', 
            context
        )


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