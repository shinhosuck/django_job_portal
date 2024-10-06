from django.contrib import admin
from .models import Company, Job, Message


@admin.register(Company)
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

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'created'
    ]