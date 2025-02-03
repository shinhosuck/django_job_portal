from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import (
    RegisterForm, 
    LoginForm, 
    ProfileUpdateForm
)
from django.contrib import messages
from django.contrib.auth import (
    login, 
    authenticate, 
    logout
)
from candidates.models import CandidateQualification
from .models import Profile
from utils.decorators import user_login_required

def register_view(request):
    next = request.GET.get('next') or None

    if request.user.is_authenticated:
        messages.warning(request, "You are already registered and logged in!")
        return redirect('candidates:jobs')

    form = RegisterForm(request.POST or None)

    context = {
        'form':form,
    }

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully registered!')

            if next:
                return redirect(f'/login/?next={next}')
            return redirect('accounts:login')
            
    return render(request, 'accounts/register.html', context)


def login_view(request): 
    next = request.GET.get('next') or None
    form = LoginForm(request.POST or None)
    context = {'form': form}

    if request.user.is_authenticated:
        user_type  = request.user.profile.user_type

        # if not user_type:
        #     messages.info(request, 'Please complete your profile to better serve you.')
        #     return redirect('accounts:profile-update')

        messages.warning(request, 'You are already authenticated.')
        if user_type == 'employer':
            return redirect('employers:employer')
        return redirect('candidates:jobs') 

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            user = authenticate(
                request, 
                username=data['username'], 
                password=data['password']
            )
            if user:
                login(request, user)
                if next:
                    return redirect(next)
                else:
                    if user.profile.user_type:
                        if user.profile.user_type == 'job seeker':
                            educations = None 
                            experiences = None

                            try:    
                                qualification = user.profile.candidatequalification 
                            except CandidateQualification.DoesNotExist:
                                qualification = None

                            if qualification:
                                educations = user.profile. \
                                    candidatequalification.educations.exists()
                                experiences = user.profile. \
                                    candidatequalification.experiences.exists()

                            if qualification and educations and experiences:
                                messages.success(request, 'Successfully logged in!')
                                return redirect('candidates:jobs')
                            else:
                                messages.info(request, 
                                              'Please complete the forms below to better serve you.')
                                return redirect('candidates:candidate-add-career-detail')
                            
                        elif user.profile.user_type == 'employer':
                            if user.profile.employers.exists():
                                return redirect('employers:employer')
                            else:
                                messages.info(request, 
                                              'Please complete the form below to better serve you.')
                                return redirect('employers:employer-register')
                    else:
                        return redirect('accounts:profile-update', user.profile.slug)
    return render(request, 'accounts/login.html', context)
            

@user_login_required
def profile_update_form_view(request, slug):
    print('hello world')
    message = request.GET.get('message')
    user = request.user 
    field_errors = []

    context = {
        'message': message
    }

    if user.profile.slug != slug:
        messages.error(request, "You are not authorized.")
        return redirect('candidates:jobs')
        
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        messages.error(request, 'There was a unknown server error. Please try again.')
        return redirect('candidates:jobs')
    
    form = ProfileUpdateForm(
        request.POST or None, 
        request.FILES or None, 
        instance=profile
    )

    if request.method == 'POST':
        if form.is_valid():
            profile_form = form.save()

            user_type = profile_form.user_type
            
            if user_type == 'job seeker':
                return redirect('candidates:candidate-add-career-detail')
            elif user_type == 'employer':
                return redirect('employers:employer-register')
        
        for key, errors in form.errors.items():
            for error in errors:
                field_errors.append(error)

        messages.error(request, f"{', '.join(field_errors)}")

    context['form'] = form

    return render(request, 'accounts/profile_update_form.html', context)


def logout_view(request):
    user = request.user

    if not user.is_authenticated:
        messages.error(request, "You haven't logged in yet!")
        return redirect('candidates:jobs')

    if request.method == 'POST':
        user_type = user.profile.user_type
        redirect_url = None 

        if user_type == 'employer':
            redirect_url = reverse('employers:employer')
        else:
            redirect_url = reverse('candidates:landing-page')

        logout(request)
        messages.success(request, 'Successfully logged out!')
        return redirect(redirect_url)
    return render(request, 'accounts/logout.html')


@user_login_required
def profile_view(request):
    scroll_to = request.GET.get('data_type')
    profile = request.user.profile
    qualification = None
    educations = None 
    experiences = None 

    if request.user.profile.user_type == 'employer':
        return redirect('employers:employer-profile')

    try:
        qualification = profile.candidatequalification
    except CandidateQualification.DoesNotExist:
        qualification = None 

    if qualification:
        educations = qualification.educations.all()
        experiences = qualification.experiences.all()

    resume = qualification and qualification.resume \
            and qualification.resume.url or None
    skills = qualification and qualification.skills or None

    context = {
        'skills':skills and skills.split(','),
        'resume': resume and resume.split('/')[-1],
        'profile': profile,
        'qualification': qualification,
        'educations': educations,
        'experiences': experiences,
        'scroll_to': scroll_to or '',
        'user_type': 'job_seeker'
    }
    return render(request, 'accounts/profile.html', context)
