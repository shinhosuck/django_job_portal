from django.urls import path 
from .views import (
    home_view,
    contact_view,
    about_view
)

app_name = 'jobs' 


urlpatterns = [
    path('', home_view, name='home'),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about')
]
