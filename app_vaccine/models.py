from django.db import models
from .constants import VACCINE_FOR, VACCINE_TYPE_CHOICES, BANGLADESH_DISTRICTS
from app_user.models import DoctorModel, PatientModel
from datetime import timedelta

class VaccineModel(models.Model):
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
    added_by = models.ForeignKey(DoctorModel, on_delete=models.CASCADE, related_name='vaccines')

    def calculate_dose_dates(self, start_date):
        dose_dates = [start_date + timedelta(days=self.dose_gap_days * i) for i in range(self.dose_count)]
        return [dose.strftime('%Y-%m-%d') for dose in dose_dates]

    def __str__(self) -> str:
        return self.vaccine_name

class VaccineCampaignModel(models.Model):
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
    patient_name = models.CharField(max_length=20)
    patient_age = models.PositiveIntegerField()
    vaccine = models.ForeignKey(VaccineModel, on_delete=models.CASCADE, related_name='booked_vaccine')
    first_dose_date = models.DateField()
    dose_dates = models.JSONField(default=list, blank=True)

    def save(self, *args, **kwargs):
        if not self.dose_dates:
            self.dose_dates = self.vaccine.calculate_dose_dates(self.first_dose_date)
        super(BookingModel, self).save(*args, **kwargs)

class BookingCampaignModel(models.Model):
    patient_name = models.CharField(max_length=20)
    patient_age = models.PositiveIntegerField()
    campaign_name = models.ForeignKey(VaccineCampaignModel, on_delete=models.CASCADE, related_name='booked_campaign')
    first_dose_date = models.DateField()
    dose_dates = models.JSONField(default=list, blank=True)

    def save(self, *args, **kwargs):
        if not self.dose_dates:
            self.dose_dates = self.campaign_name.campaign_vaccine.calculate_dose_dates(self.first_dose_date)
        super(BookingCampaignModel, self).save(*args, **kwargs)
        
class Comment(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE, related_name='comments')
    patient_name = models.CharField(max_length=30,default='person', blank=True)
    campaign = models.ForeignKey(VaccineCampaignModel, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('patient', 'campaign') 

    def __str__(self):
        return f"Comment by {self.patient} on {self.campaign}"