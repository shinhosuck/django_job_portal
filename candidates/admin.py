from django.contrib import admin
from .models import (
    Message, 
    Candidate,
    Education,
    Experience
)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = [
        'slug',
        'industry',
        'first_name',
        'last_name',
        'job_title'
    ]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = [
        'candidate',
        'major',
        'degree',
        'institution',
        'completion_date'
    ]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = [
        'candidate',
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
