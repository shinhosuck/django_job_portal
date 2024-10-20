from django.contrib import admin
from .models import Employer, Job


@admin.register(Employer)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'representative',
        'company',
        'slug',
        'created',
        'updated'
    ]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'company',
        'job_title',
        'slug',
        'salary',
        'created',
        'updated'
    ]
