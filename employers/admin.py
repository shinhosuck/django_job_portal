from django.contrib import admin
from .models import Employer, Job


@admin.register(Employer)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'representative',
        'company',
        'created',
        'updated'
    ]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'company',
        'job_title',
        'salary',
        'created',
        'updated'
    ]
