from django.db import models
from .constants import VACCINE_FOR, VACCINE_TYPE_CHOICES, BANGLADESH_DISTRICTS
from app_user.models import DoctorModel, PatientModel
from datetime import timedelta
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.contrib.auth.models import User
# import get_object_or_404()
from datetime import date
from django.shortcuts import get_object_or_404
class VaccineModel(models.Model):
    id = models.AutoField(primary_key=True,unique=True) 
    vaccine_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    manufacturer = models.CharField(max_length=100)
    dosage = models.DecimalField(max_digits=5, decimal_places=2, help_text='Dosage in ml')
    dose_count = models.IntegerField(help_text='Number of dosages required')
    dose_gap_days = models.IntegerField(help_text="Gap between doses in days", default=90)
    storage_temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text="Storage temperature in °C")
    expiration_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    vaccine_for = models.CharField(max_length=10, choices=VACCINE_FOR)
    vaccine_type = models.CharField(max_length=20, choices=VACCINE_TYPE_CHOICES)
    vaccine_img = models.URLField(blank=True,null=True)
    added_by = models.ForeignKey(DoctorModel, on_delete=models.CASCADE, related_name='vaccines')

    def calculate_dose_dates(self, start_date):
        dose_dates = [start_date + timedelta(days=self.dose_gap_days * i) for i in range(self.dose_count)]
        return [dose.strftime('%Y-%m-%d') for dose in dose_dates]

    def __str__(self) -> str:
        return self.vaccine_name

class VaccineCampaignModel(models.Model):
    id = models.AutoField(primary_key=True,unique=True) 
    campaign_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    campaign_vaccine = models.ForeignKey(VaccineModel, on_delete=models.CASCADE, related_name='campaigns')
    area = models.CharField(max_length=50, choices=BANGLADESH_DISTRICTS)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    target_population = models.PositiveIntegerField()
    campaign_for = models.CharField(max_length=10, choices=VACCINE_FOR)
    added_by = models.ForeignKey(DoctorModel, on_delete=models.CASCADE, related_name='campaigns')
    description = models.TextField(blank=True, null=True)
    campaign_img =  models.URLField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.campaign_name)  # Generate slug based on campaign_name or any other relevant field
        super(VaccineCampaignModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.campaign_name

class BookingModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    id = models.AutoField(primary_key=True) 
    patient_name = models.CharField(max_length=20)
    patient_age = models.PositiveIntegerField()
    vaccine = models.ForeignKey(VaccineModel, on_delete=models.CASCADE, related_name='booked_vaccine')
    first_dose_date = models.DateField(default=date.today)
    dose_dates = models.JSONField(default=list, blank=True)

    def save(self, *args, **kwargs):
        if not self.dose_dates:
            self.dose_dates = self.vaccine.calculate_dose_dates(self.first_dose_date)
        super(BookingModel, self).save(*args, **kwargs)

class BookingCampaignModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    id = models.AutoField(primary_key=True) 
    user = models.ForeignKey(PatientModel,related_name='bookCampaing',on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=20)
    patient_age = models.PositiveIntegerField()
    campaign_name = models.ForeignKey(VaccineCampaignModel, on_delete=models.CASCADE, related_name='booked_campaign')
    booked_date = models.DateField(default=date.today)
    is_booked = models.BooleanField(default=False)
    def __str__(self):
        return f"Booking by {self.patient_name} for {self.campaign_name}"
class Comment(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE, related_name='comments')
    patient_name = models.CharField(max_length=30,default='person', blank=True)
    patient_img = models.URLField(blank=True, null=True,default='person')
    campaign = models.ForeignKey(VaccineCampaignModel, on_delete=models.CASCADE, related_name='comments',default='user')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.patient} on {self.campaign}"

class VaccineTypeModel(models.Model):
    vaccine_type = models.CharField(max_length=20, choices=VACCINE_TYPE_CHOICES)
    type_img = models.URLField(blank=True,null=True)
    tye_description = models.CharField(max_length=500)
    
class TotalVaccineModel(models.Model):
    total_vaccine = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.total_vaccine} "
    
class TotalCampaignAdded(models.Model):
    total_campaign = models.PositiveIntegerField(default=0)
    campaign_target = models.PositiveBigIntegerField(default=0)
    
class TotalBookedOnCampaign(models.Model):
    total_booked = models.PositiveIntegerField(default=0)