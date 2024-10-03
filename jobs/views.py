from django.shortcuts import render



def home_view(request):
    return render(request, 'jobs/home.html', {'greeting': 'This is the home page!'})
