from django.contrib import admin
from .models import Profile 


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'username', 
        'slug',
        'first_name', 
        'last_name', 
        'user_type',
        'email', 
        'created', 
        'updated'
    ]
