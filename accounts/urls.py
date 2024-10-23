from django.urls import path 
from .views import (
    register_view, 
    login_view,
    logout_view,
    user_profile_view
)

from django.contrib.auth import views as auth_views

app_name = 'accounts'


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile_view, name='profile')
]
