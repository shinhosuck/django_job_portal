from django.urls import path 
from .views import (
    landing_page_view,
    contact_view,
    about_view,
    jobs_view
)

app_name = 'jobs' 


urlpatterns = [
    path('', landing_page_view, name='landing-page'),
    path('jobs/', jobs_view, name='jobs' ),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about')
]
