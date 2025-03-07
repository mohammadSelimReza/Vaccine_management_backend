# Generated by Django 5.1.6 on 2025-03-07 00:15

import app_user.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorModel',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='doctor', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('nid', models.IntegerField(unique=True)),
                ('phone_number', models.CharField(max_length=15, validators=[app_user.validators.validate_phone_number])),
                ('city', models.CharField(max_length=20)),
                ('street_address', models.CharField(max_length=500)),
                ('zip_code', models.IntegerField()),
                ('specialization', models.CharField(choices=[('immunology', 'Immunology'), ('infectious_diseases', 'Infectious Diseases'), ('pediatrics', 'Pediatrics'), ('public_health', 'Public Health'), ('epidemiology', 'Epidemiology'), ('virology', 'Virology'), ('microbiology', 'Microbiology'), ('preventive_medicine', 'Preventive Medicine'), ('travel_medicine', 'Travel Medicine'), ('tropical_medicine', 'Tropical Medicine'), ('pharmacology', 'Pharmacology'), ('vaccine_development', 'Vaccine Development'), ('geriatrics', 'Geriatrics'), ('internal_medicine', 'Internal Medicine'), ('family_medicine', 'Family Medicine'), ('allergy_and_immunology', 'Allergy and Immunology'), ('occupational_medicine', 'Occupational Medicine'), ('health_policy_and_management', 'Health Policy and Management'), ('clinical_research', 'Clinical Research'), ('bioinformatics', 'Bioinformatics')], max_length=50)),
                ('license_number', models.CharField(max_length=8, unique=True, validators=[app_user.validators.validate_license_number])),
                ('user_type', models.CharField(choices=[('patient', 'Patient'), ('doctor', 'Doctor')], default='doctor', max_length=10)),
                ('user_photo', models.URLField(blank=True, max_length=255, null=True)),
                ('is_valid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PatientModel',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='patients', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('nid', models.IntegerField(validators=[app_user.validators.validate_nid])),
                ('phone_number', models.CharField(max_length=15, validators=[app_user.validators.validate_phone_number])),
                ('city', models.CharField(max_length=20)),
                ('street_address', models.CharField(max_length=500)),
                ('zip_code', models.IntegerField()),
                ('user_type', models.CharField(blank=True, choices=[('patient', 'Patient'), ('doctor', 'Doctor')], default='patient', max_length=10)),
                ('user_photo', models.URLField(blank=True, max_length=255, null=True)),
                ('patient_id', models.CharField(blank=True, editable=False, max_length=6, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TotalPatientsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_patients', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
