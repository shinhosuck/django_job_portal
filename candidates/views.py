from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model 
from .forms import MessageForm, CandidateJobProfileForm, IndustryForm
from django.contrib import messages
from .models import CandidateJobProfile, Industry
from employers.models import Job 
from utils.decorators import user_login_required


User = get_user_model()


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
    industry_form = IndustryForm(
        request.POST or None, 
        request.FILES or None
        )
    candidate_form = CandidateJobProfileForm(
            request.POST or None, 
            request.FILES or None
        )
    
    context = {
            'candidate_form':candidate_form,
            'industries': industries
        }
    
    if request.method == 'POST':
        if candidate_form.is_valid() and industry_form.is_valid():
            candidate_instance = candidate_form.save(commit=False)
            candidate_instance.user = request.user
            # candidate_instance.save()

            print(candidate_form.changed_data)

            industry_name = industry_form.cleaned_data.get('industry')

            try:
                industry = Industry.objects.get(name=industry_name)
            except Industry.DoesNotExist:
                messages.error(request, 'Industry does not exists.')
                return render(request, 'candidates/candidates_register.html', context)
            
            # industry.candidate = candidate_instance
            # industry.save()

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
    jobs = Job.objects.select_related('employer')
    context = {'jobs': jobs}

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