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
            user=instance
        )


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    profile = instance.profile
    profile.username = instance.username
    profile.email = instance.email
    profile.slug = slugify(instance.username)
    profile.save()


@receiver(post_delete, sender=Profile)
def post_delete_user(sender, instance, **kwargs):
    if instance.profile_image and \
        instance.profile_image != 'profile_images/default.png':
        if os.path.exists(instance.profile_image.path):
            os.remove(instance.profile_image.path)