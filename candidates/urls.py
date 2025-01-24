from django.urls import path 
from .views import (
    landing_page_view,
    fetch_user_location_view,
   get_search_form_suggestions,
    contact_view,
    about_view,
    jobs_view,
    candidate_add_career_detail_view,
    candidate_detail_view,
    apply_to_a_job_view,
    job_search_view,
    get_form_data_view,
    prefetch_form_data_view,
    update_candidate_profile_info_view,
    save_job_view,
    filter_jobs_page_dashboard_view,
    job_detail_view
)

app_name = 'candidates' 


urlpatterns = [
    path('', landing_page_view, name='landing-page'),
    path('candidates/location/', fetch_user_location_view, name='candidate-location'),
    path('candidates/search-form/suggestions/', get_search_form_suggestions, name='suggestions'),
    path('candidates/jobs/', jobs_view, name='jobs' ),
    path('candidates/jobs/<str:slug>/detail/', job_detail_view, name='candidate-job-detail'),
    path('candidates/jobs/search/', job_search_view, name='job-search'),
    path('candidates/add/career/detail/', candidate_add_career_detail_view, name='candidate-add-career-detail'),
    path('candidates/<str:slug>/detail/', candidate_detail_view, name='candidate-detail'),
    path('candidates/apply/to/<str:slug>/', apply_to_a_job_view, name='candidate-apply'),
    path('candidates/fetch/form-data/', get_form_data_view, name='form-data'),
    path('candidates/prefetch/formdata/', prefetch_form_data_view, name="prefech-form-data"),
    path('candidates/<str:slug>/update/profile/info/', update_candidate_profile_info_view, name='candidate-update-profile-info'),
    path('hire-spot/contact/', contact_view, name='contact'),
    path('hire-spot/about/', about_view, name='about'),
    path('candidates/job/<str:slug>/save/', save_job_view, name='save-job'),
    path('candidates/jobs/filter/', filter_jobs_page_dashboard_view, name='filter-job')
]
