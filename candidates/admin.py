from django.contrib import admin
from .models import (
    Message, 
    CandidateQualification,
    Education,
    Experience
)


@admin.register(CandidateQualification)
class CandidateQualificationAdmin(admin.ModelAdmin):
    list_display = [
        'profile',
        'slug',
        'industry',
        'job_title'
    ]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = [
        'qualification',
        'slug',
        'major',
        'degree',
        'institution',
        'completion_date'
    ]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = [
        'qualification',
        'slug',
        'company_name',
        'position',
        'start_date',
        'end_date'
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
