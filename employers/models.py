from typing import Iterable
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from datetime import datetime
import re


User = settings.AUTH_USER_MODEL

class Employer(models.Model):
    representative = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True
    )
    employer_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    about_employer = models.TextField()
    website = models.URLField(max_length=300)
    logo = models.ImageField(
        upload_to='company_logos', 
        default='company_logos/default.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employer_name']

    def get_absolute_url(self):
        return reverse("employers:employer-detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.employer_name
    
    
class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    salary = models.DecimalField(max_digits=100, decimal_places=2)
    qualification = models.TextField()
    applicants = models.ManyToManyField(User, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.job_title)}-'+''.join(re.findall('\d', str(datetime.now())))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("employers:job-detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.job_title
