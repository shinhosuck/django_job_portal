from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


def user_login_required(fn):

    def wrapper( request, *args, **kwargs):
        path = request.path
        redirect_url = f'{reverse("accounts:login")}?next={path}'

        if not request.user.is_authenticated:
            messages.error(request, "Please login to preceed to requested page.")
            return redirect(redirect_url)
        
        return fn(request, *args, **kwargs)

    return wrapper