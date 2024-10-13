from django.urls import path 
from .views import (
    employer_view, 
    employer_register,
    post_job_view
)

app_name = 'employers'


urlpatterns = [
    path('recruit/', employer_view, name='employer'),
    path('employers/register/', employer_register, name='employer-register'),
    path('post/job/', post_job_view, name='post-job')
]
