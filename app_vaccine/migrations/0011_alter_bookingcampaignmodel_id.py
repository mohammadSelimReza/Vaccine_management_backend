# Generated by Django 5.1 on 2024-09-06 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_vaccine', '0010_totalbookedoncampaign_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingcampaignmodel',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]