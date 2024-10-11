from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

class Company(models.Model):
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
        verbose_name_plural = 'Companies'
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
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=100, decimal_places=2)
    applicants = models.ManyToManyField(User, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category']

    def __str__(self):
        return self.job_title
    

class Message(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        editable=False, 
        default=uuid.uuid4
    )
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
    
