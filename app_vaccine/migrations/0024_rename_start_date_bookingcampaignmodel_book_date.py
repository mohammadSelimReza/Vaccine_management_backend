# Generated by Django 5.1 on 2024-09-02 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_vaccine', '0023_rename_first_dose_date_bookingcampaignmodel_start_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookingcampaignmodel',
            old_name='start_date',
            new_name='book_date',
        ),
    ]
