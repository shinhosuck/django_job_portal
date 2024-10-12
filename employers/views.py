from django.shortcuts import render



def employer_view(request):
    return render(request, 'employers/employers_landing_page.html', {})
