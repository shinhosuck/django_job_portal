# Generated by Django 5.1.1 on 2024-10-20 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0002_alter_job_options_employer_slug_alter_employer_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
    ]
