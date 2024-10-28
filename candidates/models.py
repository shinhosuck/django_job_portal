from typing import Any
from django.db import models
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class CandidateJobProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200)
    job_title = models.CharField(max_length=200)
    skills = models.CharField(max_length=300, blank=True, null=True)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    social_link = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Candidate Job Profiles'

    def __str__(self):
        return f'{self.user.username}'  

    def get_absolute_url(self):
        return reverse('candidates:candidate-detail', kwargs={'slug': self.slug})

    def get_resume_url(self, request=None):
        if request:
            return request.build_absolute_uri(self.resume.url)
        return self.resume.url


class Industry(models.Model):
    candidate = models.ForeignKey(
            CandidateJobProfile, 
            on_delete=models.CASCADE,
            null=True, 
            blank=True
        )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Industries'

    def __str__(self):
        return self.name


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
    
