from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL


class Candidate(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        editable=False, 
        default=uuid.uuid4
    )
    avatar = models.ImageField(upload_to='avatars', default='avatars/default.png')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=200)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    social_link = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}'  

    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})

    def get_resume_url(self, request=None):
        if request:
            return request.build_absolute_uri(self.resume.url)
        return self.resume.url
      
    

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
    
