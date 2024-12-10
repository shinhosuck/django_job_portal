from django.urls import path 
from .views import (
    employer_landing_page_view, 
    employer_register,
    post_job_view,
    employer_profile_view,
    employer_detail_view,
    employer_job_detail,
    employer_job_update_view,
    employer_update_view
)

app_name = 'employers'


urlpatterns = [
    path('employers/', employer_landing_page_view, name='employer'),
    path('employers/register/', employer_register, name='employer-register'),
    path('employers/post/job/', post_job_view, name='post-job'),
    path('employers/profile/', employer_profile_view, name='employer-profile'),
    path('employers/<str:slug>/detail/', employer_detail_view, name='employer-detail'),
    path('employers/jobs/<str:slug>/detail/', employer_job_detail, name='job-detail'),
    path('employers/job/<str:slug>/update/', employer_job_update_view, name='job-update'),
    path('employers/<str:slug>/update/', employer_update_view, name="update-employer")
]
