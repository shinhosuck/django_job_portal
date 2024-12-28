from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from datetime import datetime
from django_countries.fields import CountryField
from candidates.models import CandidateQualification
from utils.constant import (
    JOB_TYPE_CHOICES, 
    EXPERIENCE_LEVEL_CHOICES, 
    WORK_LOCATION_CHOICES,
    INDUSTRY_CHOICES,
    PAYMENT_TYPE_CHOICES
)
from accounts.models import Profile
import re


User = settings.AUTH_USER_MODEL

class Employer(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, 
        null=True, blank=True, related_name='employers')
    logo = models.ImageField(
        upload_to='company_logos', default='company_logos/default.png')
    employer_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200)
    state_or_province = models.CharField(max_length=200)
    country = CountryField()
    zip_code_or_postal_code = models.CharField(max_length=50)
    website = models.URLField(
            max_length=300, null=True, blank=True, 
            help_text='Website address must start with https:// follow by www.company.com'
        )
    about_employer = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employer_name']

    def get_logo_url(self):
        return self.logo.url

    def get_absolute_url(self):
        return reverse("employers:employer-detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.employer_name
    
    
class Job(models.Model):
    employer = models.ForeignKey(
        Employer, 
        on_delete=models.CASCADE, 
        related_name='jobs'
    )
    industry = models.CharField(choices=INDUSTRY_CHOICES ,max_length=100)
    job_title = models.CharField(max_length=200)
    job_type = models.CharField(choices=JOB_TYPE_CHOICES, max_length=100)
    experience_level = models.CharField(choices=EXPERIENCE_LEVEL_CHOICES, max_length=100)
    work_location = models.CharField(choices=WORK_LOCATION_CHOICES, max_length=100)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES)
    currency = CountryField()
    salary = models.DecimalField(max_digits=100, decimal_places=2)
    currency_code = models.CharField(max_length=10)
    job_description = models.TextField()
    qualification = models.TextField()
    applicants = models.ManyToManyField(CandidateQualification, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.job_title)}-'+''.join(re.findall('\d', str(datetime.now())))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("employers:job-detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.job_title
