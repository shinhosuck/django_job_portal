from typing import Iterable
from django.db import models
from django.conf import settings 
from django.utils.text import slugify
import uuid

User = settings.AUTH_USER_MODEL 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField()
    avatar = models.ImageField(upload_to='avatars', default='avatars/default.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'avatars/default.png'

        if not self.slug:
            self.slug = slugify(self.username)

        return super().save(*args, **kwargs)
    
    def get_avatar_url(self):
        return self.avatar.url

    def __str__(self):
        return self.username
    

