from django.urls import path 
from .views import (
    landing_page_view,
    contact_view,
    about_view,
    jobs_view,
    candidate_register_view,
    candidate_detail_view,
    apply_to_a_job_view,
    job_search_view,
    fetch_user_location,
    get_search_form_suggestions
)

app_name = 'candidates' 


urlpatterns = [
    path('', landing_page_view, name='landing-page'),
    path('candidates/jobs/', jobs_view, name='jobs' ),
    path('candidates/jobs/search/', job_search_view, name='job-search'),
    path('candidates/register/', candidate_register_view, name='candidate-register'),
    path('candidates/<str:slug>/detail/', candidate_detail_view, name='candidate-detail'),
    path('candidates/apply/to/<str:slug>/', apply_to_a_job_view, name='candidate-apply'),
    path('candidates/location/', fetch_user_location, name='candidate-location'),
    path('hire-spot/contact/', contact_view, name='contact'),
    path('hire-spot/about/', about_view, name='about'),
    path('candidates/search-form/suggestions/', get_search_form_suggestions, name='suggestions')
]
