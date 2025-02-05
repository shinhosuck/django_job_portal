from django.db import models
from django.conf import settings 
from utils.constant import USER_TYPE_CHOICES
from django.urls import reverse
from django_countries.fields import CountryField

User = settings.AUTH_USER_MODEL 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to='profile_images', default='profile_images/default.png')
    slug = models.SlugField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state_or_province = models.CharField(max_length=50)
    country = CountryField()
    post_code_or_zip_code = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    social_link = models.URLField(null=True, blank=True)
    personal_website = models.URLField(blank=True, null=True)
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        profile_id = self.id or None

        if not self.profile_image:
            self.profile_image = 'profile_images/default.png'

        super().save(*args, **kwargs)

        if profile_id:
            if self.username == self.user.username and \
            self.email == self.user.email:
                pass
            else:
                
                if self.user.username != self.username:
                    self.user.username = self.username 
                
                if self.user.email != self.email:
                    self.user.email = self.email

                self.user.save()
        return None
        
    def get_profile_image_url(self):
        return self.profile_image.url

    def get_absolute_url(self):
        return reverse("accounts:profile-update", kwargs={"slug": self.slug})
    

class AppliedJob(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='applied_jobs')
    applied_job = models.ForeignKey('employers.job', on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.applied_job}'


class SavedJob(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='saved_jobs')
    saved_job = models.ForeignKey('employers.job', on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.saved_job}'