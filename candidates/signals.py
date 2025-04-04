from django.db.models.signals import post_delete, post_save
from candidates.models import CandidateQualification
from django.dispatch import receiver
from django.utils.text import slugify
from datetime import datetime
import os
import re


@receiver(post_save, sender=CandidateQualification)
def post_save_candidate(sender, instance, created, **kwargs):

    if created:
        instance.slug = f'{slugify(instance.profile.user.username)}-'+ \
        ''.join(re.findall('\d', str(datetime.now())))
        instance.save()


@receiver(post_delete, sender=CandidateQualification)
def post_delete_candidate(sender, instance, **kwargs):

    if instance.resume:
        if os.path.exists(instance.resume.path):
            os.remove(instance.resume.path)