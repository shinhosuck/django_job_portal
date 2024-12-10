from django.contrib import admin
from .models import Profile, AppliedJob, SavedJob


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'username', 
        'user_type',
        'slug',
        'first_name', 
        'last_name', 
        'user_type',
        'email', 
        'created', 
        'updated'
    ]


@admin.register(AppliedJob)
class AppliedJobAdmin(admin.ModelAdmin):
    list_display = ['profile', 'applied_job', 'created']


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['profile', 'saved_job', 'created']
