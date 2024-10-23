from django.db.models.signals import post_delete, post_save
from candidates.models import Candidate
from django.dispatch import receiver
from django.utils.text import slugify
import os


@receiver(post_save, sender=Candidate)
def post_save_candidate(sender, instance, created, **kwargs):
    if created:
        instance.slug = slugify(instance.user.username)
        instance.save()


@receiver(post_delete, sender=Candidate)
def post_delete_candidate(sender, instance, **kwargs):

    if instance.avatar and instance.avatar != 'avatars/default.png':
        if os.path.exists(instance.avatar.path):
            os.remove(instance.avatar.path)

    if instance.resume:
        if os.path.exists(instance.resume.path):
            os.remove(instance.resume.path)