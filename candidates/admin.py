from django.contrib import admin
from .models import (
    Message, 
    CandidateJobProfile
)


@admin.register(CandidateJobProfile)
class CandidateJobProfileAdmin(admin.ModelAdmin):
    list_display = [
        'slug',
        'industry',
        'first_name',
        'last_name',
        'job_title'
    ]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'created'
    ]
