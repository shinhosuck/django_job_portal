from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model 
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import json

from .forms import (
    MessageForm, 
    CandidateForm,
    EducationForm,
    ExperienceForm
)

from .models import (
    Candidate,
    Education,
    Experience
)
from employers.models import Job 

# Utils
from utils.decorators import user_login_required
from utils.geo_location import get_user_ip
from utils.handle_suggestions import generate_suggestions
from utils.create_candiate_profile import (
    create_or_update_candidate_info, 
    create_or_update_candidate_education,
    create_or_update_candidate_experience,
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
    country =  get_user_ip(request)['country']

    values = Job.objects.filter(employer__country=country).\
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
def candidate_register_view(request):
    user = request.user
    data_type = request.GET.get('type')

    try:
        candidate = Candidate.objects.get(user=user)
    except Candidate.DoesNotExist:
        candidate = None

    candidate_form = candidate and \
          CandidateForm(instance=candidate) or CandidateForm()
    file = candidate and  candidate.get_resume_url()

    print(file)
    
    
    if request.method == 'POST':
        if data_type == 'candidate_info':
            data = request.POST
            resume = request.FILES.get('resume')
            profile = user.profile

            context = create_or_update_candidate_info(
                data, resume, user, profile, 'candidate_info')
           
            return JsonResponse(context)
    
        if data_type == 'education':
            data = request.POST
            context = create_or_update_candidate_education(data, request, 'education')

            return JsonResponse(context)
        
        if data_type == 'experience':
            data = request.POST
            context = create_or_update_candidate_experience(data, request, 'experience')

            return JsonResponse(context)
    
    context = {
            'candidate_form':candidate_form,
            'file': file
        }
       
    return render(request, 'candidates/candidates_register.html', context)


def get_form_data_view(request):
    data = json.loads(request.body.decode('utf-8'))

    education = data.get('education')
    experience = data.get('experience')

    context = fetch_previous_form_data(education, experience)

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

    return render(request, 'candidates/candidates_detail.html', context)


def jobs_view(request):
    data = get_user_ip(request)
    jobs = Job.objects.select_related('employer')
    user = request.user
    context = {}

    country = data['country']
    city = data['city']

    if request.user.is_authenticated:
        candidate_job_titles = Candidate.objects.\
            filter(user=user).values_list('job_title', flat=True)
        
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
        candidate = Candidate.objects.get(user=user)
    except Candidate.DoesNotExist:
        messages.error(request, 'You must create your profile first.')
        return redirect('candidates:candidate-register')
    
    job.applicants.add(candidate)

    messages.success(request, f'Successfully applied to {job.job_title}.')
    return redirect('candidates:jobs')


def job_search_view(request):
    search = request.GET.get('q') or None
    
    return render(request, 'candidates/candidates_search_results.html')


