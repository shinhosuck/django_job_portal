# Generated by Django 5.1.1 on 2024-12-04 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='post_code_or_zip_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]