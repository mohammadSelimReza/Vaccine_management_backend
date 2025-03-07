# Generated by Django 5.1.6 on 2025-03-07 00:15

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BannerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('banner_img', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='banner_img')),
            ],
        ),
        migrations.CreateModel(
            name='TestimonialModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=255)),
            ],
        ),
    ]
