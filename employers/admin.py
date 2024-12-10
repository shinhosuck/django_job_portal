from django.contrib import admin
from .models import Employer, Job


@admin.register(Employer)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'profile',
        'employer_name',
        'slug',
        'created',
        'updated'
    ]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'employer',
        'job_title',
        'slug',
        'salary',
        'created',
        'updated'
    ]
