# Generated by Django 5.1.1 on 2024-10-28 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='avatar',
            new_name='profile_image',
        ),
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]