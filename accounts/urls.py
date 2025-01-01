from django.urls import path 
from .views import (
    register_view, 
    login_view,
    logout_view,
    profile_update_form_view,
    profile_view,
)

from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/update/', profile_update_form_view, name='profile-update'),
    path('profile/', profile_view, name='profile'),
]
