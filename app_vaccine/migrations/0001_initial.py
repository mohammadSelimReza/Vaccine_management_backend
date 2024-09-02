# Generated by Django 5.1 on 2024-09-02 21:25

import cloudinary.models
import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_user', '0009_alter_doctormodel_street_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VaccineTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine_type', models.CharField(choices=[('inactivated', 'Inactivated Vaccine'), ('live_attenuated', 'Live Attenuated Vaccine'), ('subunit', 'Subunit Vaccine'), ('mRNA', 'mRNA Vaccine'), ('viral_vector', 'Viral Vector Vaccine'), ('toxoid', 'Toxoid Vaccine'), ('hepatitis_b', 'Hepatitis B'), ('live_attenuated', 'Live attenuated'), ('recombinant', 'Recombinant'), ('inactivated_toxin', 'Inactivated toxin')], max_length=20)),
                ('type_img', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='type_img')),
                ('tye_description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='VaccineCampaignModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=60, unique=True)),
                ('area', models.CharField(choices=[('Barguna', 'Barguna'), ('Barishal', 'Barishal'), ('Bhola', 'Bhola'), ('Jhalokathi', 'Jhalokathi'), ('Patuakhali', 'Patuakhali'), ('Pirojpur', 'Pirojpur'), ('Bandarban', 'Bandarban'), ('Brahmanbaria', 'Brahmanbaria'), ('Chandpur', 'Chandpur'), ('Chattogram', 'Chattogram'), ('Cumilla', 'Cumilla'), ('Coxs_Bazar', 'Coxs_Bazar'), ('Feni', 'Feni'), ('Khagrachari', 'Khagrachari'), ('Lakshmipur', 'Lakshmipur'), ('Noakhali', 'Noakhali'), ('Rangamati', 'Rangamati'), ('Dhaka', 'Dhaka'), ('Faridpur', 'Faridpur'), ('Gazipur', 'Gazipur'), ('Gopalganj', 'Gopalganj'), ('Kishoreganj', 'Kishoreganj'), ('Madaripur', 'Madaripur'), ('Manikganj', 'Manikganj'), ('Munshiganj', 'Munshiganj'), ('Narayanganj', 'Narayanganj'), ('Narsingdi', 'Narsingdi'), ('Rajbari', 'Rajbari'), ('Shariatpur', 'Shariatpur'), ('Tangail', 'Tangail'), ('Bagerhat', 'Bagerhat'), ('Chuadanga', 'Chuadanga'), ('Jashore', 'Jashore'), ('Jhenaidah', 'Jhenaidah'), ('Khulna', 'Khulna'), ('Kushtia', 'Kushtia'), ('Magura', 'Magura'), ('Meherpur', 'Meherpur'), ('Narail', 'Narail'), ('Satkhira', 'Satkhira'), ('Jamalpur', 'Jamalpur'), ('Mymensingh', 'Mymensingh'), ('Netrokona', 'Netrokona'), ('Sherpur', 'Sherpur'), ('Bogura', 'Bogura'), ('Joypurhat', 'Joypurhat'), ('Naogaon', 'Naogaon'), ('Natore', 'Natore'), ('Chapai_Nawabganj', 'Chapai Nawabganj'), ('Pabna', 'Pabna'), ('Rajshahi', 'Rajshahi'), ('Sirajganj', 'Sirajganj'), ('Dinajpur', 'Dinajpur'), ('Gaibandha', 'Gaibandha'), ('Kurigram', 'Kurigram'), ('Lalmonirhat', 'Lalmonirhat'), ('Nilphamari', 'Nilphamari'), ('Panchagarh', 'Panchagarh'), ('Rangpur', 'Rangpur'), ('Thakurgaon', 'Thakurgaon'), ('Habiganj', 'Habiganj'), ('Maulvibazar', 'Maulvibazar'), ('Sunamganj', 'Sunamganj'), ('Sylhet', 'Sylhet')], max_length=50)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('target_population', models.PositiveIntegerField()),
                ('campaign_for', models.CharField(choices=[('adult', 'Adult'), ('child', 'Child')], max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('campaign_img', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='campaign_img')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='app_user.doctormodel')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(blank=True, default='person', max_length=30)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app_user.patientmodel')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app_vaccine.vaccinecampaignmodel')),
            ],
        ),
        migrations.CreateModel(
            name='BookingCampaignModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=20)),
                ('patient_age', models.PositiveIntegerField()),
                ('booked_date', models.DateField(default=datetime.date.today)),
                ('is_booked', models.BooleanField(default=False)),
                ('campaign_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_campaign', to='app_vaccine.vaccinecampaignmodel')),
            ],
        ),
        migrations.CreateModel(
            name='VaccineModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine_name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, max_length=60, unique=True)),
                ('manufacturer', models.CharField(max_length=100)),
                ('dosage', models.DecimalField(decimal_places=2, help_text='Dosage in ml', max_digits=5)),
                ('dose_count', models.IntegerField(help_text='Number of dosages required')),
                ('dose_gap_days', models.IntegerField(default=90, help_text='Gap between doses in days')),
                ('storage_temperature', models.DecimalField(decimal_places=1, help_text='Storage temperature in °C', max_digits=4)),
                ('expiration_date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('vaccine_for', models.CharField(choices=[('adult', 'Adult'), ('child', 'Child')], max_length=10)),
                ('vaccine_type', models.CharField(choices=[('inactivated', 'Inactivated Vaccine'), ('live_attenuated', 'Live Attenuated Vaccine'), ('subunit', 'Subunit Vaccine'), ('mRNA', 'mRNA Vaccine'), ('viral_vector', 'Viral Vector Vaccine'), ('toxoid', 'Toxoid Vaccine'), ('hepatitis_b', 'Hepatitis B'), ('live_attenuated', 'Live attenuated'), ('recombinant', 'Recombinant'), ('inactivated_toxin', 'Inactivated toxin')], max_length=20)),
                ('vaccine_img', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='vaccine_img')),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccines', to='app_user.doctormodel')),
            ],
        ),
        migrations.AddField(
            model_name='vaccinecampaignmodel',
            name='campaign_vaccine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='app_vaccine.vaccinemodel'),
        ),
        migrations.CreateModel(
            name='BookingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=20)),
                ('patient_age', models.PositiveIntegerField()),
                ('first_dose_date', models.DateField()),
                ('dose_dates', models.JSONField(blank=True, default=list)),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_vaccine', to='app_vaccine.vaccinemodel')),
            ],
        ),
    ]
