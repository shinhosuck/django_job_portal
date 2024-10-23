from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from accounts.models import Profile
from django.dispatch import receiver
from django.utils.text import slugify
import os


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance, 
        )

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.username = instance.username
    instance.profile.email = instance.email
    instance.profile.slug = slugify(instance.username)
    instance.profile.save()


@receiver(post_delete, sender=Profile)
def post_delete_user(sender, instance, **kwargs):
    if instance.avatar and instance.avatar != 'avatars/default.png':
        if os.path.exists(instance.avatar.path):
            os.remove(instance.avatar.path)