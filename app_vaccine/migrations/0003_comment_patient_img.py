# Generated by Django 5.1 on 2024-09-03 15:51

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_vaccine', '0002_rename_book_date_bookingmodel_first_dose_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='patient_img',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='campaign_img'),
        ),
    ]
