# Generated by Django 5.1.1 on 2024-12-05 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0011_job_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='currency_code',
            field=models.CharField(default='none', max_length=10),
            preserve_default=False,
        ),
    ]