# Generated by Django 5.0.9 on 2025-02-17 08:42

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_profile_contact_info_alter_profile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dzuro3ezl/image/upload/v1739781463/easygrocery/user/avatar_qpkqzn.png', max_length=255, verbose_name='image'),
        ),
    ]
