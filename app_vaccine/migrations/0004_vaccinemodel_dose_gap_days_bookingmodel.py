# Generated by Django 5.1 on 2024-08-23 15:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0005_alter_doctormodel_user_type'),
        ('app_vaccine', '0003_alter_vaccinecampaignmodel_campaign_vaccine'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaccinemodel',
            name='dose_gap_days',
            field=models.IntegerField(default='90', help_text='Gap between doses in days'),
        ),
        migrations.CreateModel(
            name='BookingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_dose_date', models.DateField()),
                ('dose_dates', models.JSONField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_book', to='app_user.patientmodel')),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_vaccine', to='app_vaccine.vaccinemodel')),
            ],
        ),
    ]
