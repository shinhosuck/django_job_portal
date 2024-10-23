from django.urls import path 
from .views import (
    landing_page_view,
    contact_view,
    about_view,
    jobs_view,
    candidate_register_view,
    candidate_detail_view
)

app_name = 'candidates' 


urlpatterns = [
    path('', landing_page_view, name='landing-page'),
    path('candidates/register/', candidate_register_view, name='candidate-register'),
    path('candidates/<str:slug>/detail/', candidate_detail_view, name='candidate-detail'),
    path('jobs/', jobs_view, name='jobs' ),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about'),

]
