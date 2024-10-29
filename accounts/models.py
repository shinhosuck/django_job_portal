from typing import Iterable
from django.db import models
from django.conf import settings 
from django.utils.text import slugify
from candidates.models import CandidateJobProfile

User = settings.AUTH_USER_MODEL 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images', default='profile_images/default.png')
    username = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField()
    user_type = models.CharField(max_length=100, null=True, blank=True)
    job_profiles = models.ManyToManyField(CandidateJobProfile, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.profile_image:
            self.profile_image = 'profile_images/default.png'

        if not self.slug:
            self.slug = slugify(self.username)

        return super().save(*args, **kwargs)
    
    def get_profile_image_url(self):
        return self.profile_image.url

    def __str__(self):
        return self.username
    

