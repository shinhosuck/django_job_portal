from django.contrib import admin
from .models import Profile 


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'username', 
        'first_name', 
        'last_name', 
        'email', 
        'created', 
        'updated'
    ]
