# Generated by Django 5.1 on 2024-08-23 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_vaccine', '0006_remove_bookingmodel_dose_dates'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingmodel',
            name='dose_dates',
            field=models.JSONField(default=None),
        ),
    ]
