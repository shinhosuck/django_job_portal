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
)

app_name = 'candidates' 


urlpatterns = [
    path('', landing_page_view, name='landing-page'),
    path('jobs/', jobs_view, name='jobs' ),
    path('jobs/search/', job_search_view, name='job-search'),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about'),
    path('candidates/register/', candidate_register_view, name='candidate-register'),
    path('candidates/<str:slug>/detail/', candidate_detail_view, name='candidate-detail'),
    path('candidates/apply/to/<str:slug>/', apply_to_a_job_view, name='candidate-apply'),

]
