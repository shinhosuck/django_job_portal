from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

class Employer(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        editable=False, 
        default=uuid.uuid4
    )
    representative = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True
    )
    company = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company_logos')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['company']

    def __str__(self):
        return self.company
    
    
class Job(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        editable=False, 
        default=uuid.uuid4
    )
    category = models.CharField(max_length=50)
    company = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=100, decimal_places=2)
    applicants = models.ManyToManyField(User, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category']

    def __str__(self):
        return self.job_title
