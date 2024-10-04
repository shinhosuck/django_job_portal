from django.shortcuts import render
from accounts.models import Profile
from django.contrib.auth import get_user_model 
from django.contrib.auth.decorators import login_required

User = get_user_model()


def home_view(request):
    return render(request, 'jobs/home.html', {'greeting': 'This is the home page!'})
