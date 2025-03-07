from django.db import models
from django.conf import settings
from django.urls import reverse
from utils.constant import INDUSTRY_CHOICES
from accounts.models import Profile

from datetime import datetime 

User = settings.AUTH_USER_MODEL

class CandidateQualification(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    industry = models.CharField(choices=INDUSTRY_CHOICES, max_length=200)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    job_title = models.CharField(max_length=200)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    skills = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile.user.username}'  

    def get_absolute_url(self):
        return reverse('candidates:candidate-detail', kwargs={'slug': self.slug})

    def get_resume_url(self, request=None):
        if self.resume:
            if request:
                return request.build_absolute_uri(self.resume.url)
            return self.resume.url
    

class Education(models.Model):
    qualification = models.ForeignKey(
            CandidateQualification, on_delete=models.CASCADE, 
            related_name='educations', null=True, blank=True
        )
    slug = models.SlugField(max_length=100, null=True, blank=True)
    major = models.CharField(max_length=255, null=True, blank=True)
    degree = models.CharField(max_length=255, null=True, blank=True)
    institution = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.degree
    
    def save(self, *args, **kwargs):
        nums = [str(num) for num in range(0, 10)]
        str_dt = ''.join([char for char in str(datetime.now()) if char in nums])
        
        if not self.slug:
            user = self.qualification.profile.username
            self.slug =f'{user}-education-{str_dt}'
            
        return super().save(*args, **kwargs)
    

class Experience(models.Model):
    qualification = models.ForeignKey(
            CandidateQualification, on_delete=models.CASCADE, 
            related_name='experiences', null=True, blank=True
        )
    slug = models.SlugField(max_length=100, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.company_name
    
    def save(self, *args, **kwargs):
        nums = [str(num) for num in range(0, 10)]
        str_dt = ''.join([char for char in str(datetime.now()) if char in nums])
        
        if not self.slug:
            user = self.qualification.profile.username
            self.slug =f'{user}-experience-{str_dt}'

        return super().save(*args, **kwargs)
    
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        if self.user:
            return self.user.username
        return f'{self.first_name} {self.last_name}'
    
