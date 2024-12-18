# Generated by Django 5.1.1 on 2024-11-26 19:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0005_alter_education_qualification_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='qualification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='educations', to='candidates.candidatequalification'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='qualification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='candidates.candidatequalification'),
        ),
    ]
