# Generated by Django 5.1.1 on 2024-12-04 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_profile_post_code_or_zip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='post_code_or_zip_code',
            field=models.CharField(max_length=50),
        ),
    ]
