from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model 
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

from .forms import MessageForm, CandidateJobProfileForm

from .models import CandidateJobProfile, Industry
from employers.models import Job 

from utils.decorators import user_login_required
from utils.geo_location import get_user_ip
from utils.handle_suggestions import generate_suggestions

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
    industries = Industry.objects.all()
    user = request.user

    candidate_form = CandidateJobProfileForm(
            request.POST or None, 
            request.FILES or None
        )
    
    context = {
            'candidate_form':candidate_form,
            'industries': industries
        }
    
    if request.method == 'POST':
        if candidate_form.is_valid():
            candidate_instance = candidate_form.save(commit=False)
            candidate_instance.user = request.user
            candidate_instance.save()
            
            user.profile.job_profiles.add(candidate_instance)

            messages.success(request, 'Profile successfully created.')
            return redirect('candidates:jobs')
        else:
            messages.error(request, 'Something went wrong. Please try again.')
       
    return render(request, 'candidates/candidates_register.html', context)


def candidates_view(request):
    candidates = CandidateJobProfile.objects.all()

    context = {'candidates': candidates}

    return render(request, 'candidates/candidates.html', context)


def candidate_detail_view(request, slug):
    context = {}

    try:
        candidate = CandidateJobProfile.objects.get(slug=slug)
    except CandidateJobProfile.DoesNotExist:
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
        candidate_job_titles = CandidateJobProfile.objects.\
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
        candidate = CandidateJobProfile.objects.get(user=user)
    except CandidateJobProfile.DoesNotExist:
        messages.error(request, 'You must create your profile first.')
        return redirect('candidates:candidate-register')
    
    job.applicants.add(candidate)

    messages.success(request, f'Successfully applied to {job.job_title}.')
    return redirect('candidates:jobs')


def job_search_view(request):
    search = request.GET.get('q') or None
    
    return render(request, 'candidates/candidates_search_results.html')