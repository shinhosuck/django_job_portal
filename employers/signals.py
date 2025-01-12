from django.db.models.signals import post_save, post_delete
from .models import Employer
from django.dispatch import receiver
from django.utils.text import slugify
import os


@receiver(post_save, sender=Employer)
def post_save_employer(sender, instance, created, **kwargs):
    if created:
        instance.slug = slugify(instance.employer_name)
        instance.save()


@receiver(post_save, sender=Employer)
def post_save_employer(sender, instance, created, **kwargs):
    if not instance.logo:
        instance.logo = 'company_logos/default.png'
        instance.save()


@receiver(post_delete, sender=Employer)
def post_delete_employer(sender, instance, **kwargs):
    if instance.logo and instance.logo != 'company_logos/default.png':
        if os.path.exists(instance.logo.path):
            os.remove(instance.logo.path)