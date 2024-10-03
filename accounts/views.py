from django.shortcuts import render


def register_view(request):
    return render(request, 'accounts/register.html', {})
