from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model 
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import json

from accounts.models import Profile
from django.urls import reverse

from .forms import MessageForm
from .models import (
    CandidateQualification,
    Education,
    Experience
)
from employers.models import Job 

# Utils
from utils.decorators import user_login_required
from utils.geo_location import get_user_ip
from utils.handle_suggestions import generate_suggestions
from utils.create_candiate_profile import (
    create_or_update_qualification, 
    create_or_update_education,
    create_or_update_experience,
    fetch_previous_form_data,
    prefetch_form_data
)


User = get_user_model()


def fetch_user_location(request):
    location = get_user_ip(request)
    return JsonResponse(location, status=200)


def get_search_form_suggestions(request):
    search = request.GET.get('q')
    city = request.GET.get('city')
    location =  get_user_ip(request)

    values = Job.objects.filter(employer__country=location['country']).\
        values('job_title','industry','job_type','employer__city')
    
    suggestions = generate_suggestions(values, search, city)
    
    return JsonResponse(suggestions, status=200)


def landing_page_view(request):
    if request.user.is_authenticated:
        return redirect('candidates:jobs')
    return render(request, 'candidates/candidates_landing_page.html')


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


@user_login_required
def candidate_add_career_detail_view(request):
    user = request.user
    data_type = request.GET.get('type')
    data = request.POST

    try:
        resume = user.profile.candidatequalification\
        .get_resume_url()
    except CandidateQualification.DoesNotExist:
        resume = None

    if not request.user.profile.user_type:
        message = '?message=Please complete your profile.'
        return redirect(f'{reverse('accounts:profile-update')}{message}')
    
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
        
    context = {'resume': resume or ''}
    
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
        {'error':'You must login first.'}
    }
    return JsonResponse

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
    data = get_user_ip(request)
    jobs = Job.objects.select_related('employer')
    user = request.user
    context = {}

    country = data['country']
    city = data['city']

    if request.user.is_authenticated:
        candidate_job_titles =CandidateQualification.objects.\
            filter(profile=user.profile).values_list('job_title', flat=True)
        
        filtered = ''
        
        if candidate_job_titles:
            for job_title in candidate_job_titles:
                for title in job_title.split(' '):
                    if not filtered:
                        if not city:
                            filtered = jobs.filter(Q(
                                job_title__icontains=title, 
                                employer__country=country
                            ))
                        else:
                             filtered = jobs.filter(Q(
                                job_title__icontains=title, 
                                employer__country=country, 
                                employer__city=city
                            ))
                    else:
                        if not city:
                            filtered = filtered.union(jobs.filter(Q(
                                job_title__icontains=title,
                                employer__country=country
                            )))
                        else:
                             filtered = filtered.union(jobs.filter(Q(
                                job_title__icontains=title,
                                employer__country=country,
                                employer__city=city
                            )))
                             
            if filtered:
                context['jobs'] = filtered
    else:
        context['jobs'] = jobs.filter(employer__country=country)

    return render(request, 'candidates/candidates_jobs.html', context)


@user_login_required
def apply_to_a_job_view(request, slug):
    user = request.user
    
    try:
        job = Job.objects.get(slug=slug)
    except Job.DoesNotExist:
        messages.error(request, f'Job does not exist. Pleas try again.')
        return redirect('candidates:jobs')
    
    try:
        candidate = CandidateQualification.objects.get(user=user)
    except CandidateQualification.DoesNotExist:
        messages.error(request, 'You must create your profile first.')
        return redirect('candidates:candidate-register')
    
    job.applicants.add(candidate)

    messages.success(request, f'Successfully applied to {job.job_title}.')
    return redirect('candidates:jobs')


def job_search_view(request):
    search = request.GET.get('q') or None
    
    return render(request, 'candidates/candidates_search_results.html')


