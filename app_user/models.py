from django.db import models
from django.contrib.auth.models import User
from .validators import validate_nid,validate_phone_number,generate_unique_patient_number,validate_license_number
from .constants import GENDER_TYPE,USER_TYPE,VACCINE_SPECIALIZATIONS
from django.core.files.base import ContentFile
# Create your models here.
class PatientModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patients')
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    nid = models.IntegerField(validators=[validate_nid])
    phone_number = models.CharField(max_length=15, validators=[validate_phone_number])
    city = models.CharField(max_length=20)
    street_address = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    user_type = models.CharField(max_length=10, choices=USER_TYPE, blank=True, default='patient')
    user_photo = models.ImageField(upload_to='images/user/', blank=True,null=True)
    patient_id = models.CharField(max_length=6, unique=True, blank=True, editable=False)
    def save(self, *args, **kwargs):
        if not self.patient_id:
            self.patient_id = generate_unique_patient_number()
        if not self.user_photo:
            self.user_photo = self.get_default_photo(self.gender)
        super().save(*args, **kwargs)
    
    def get_default_photo(self, gender):
        if gender == 'male':
            default_image_path = 'images/user/male_default.png'
        elif gender == 'female':
            default_image_path = 'images/user/female_default.png'
        else:
            default_image_path = 'images/user/default_user.png'
        
        try:
            with open(default_image_path, 'rb') as image_file:
                return ContentFile(image_file.read(), 'default_photo.jpg')
        except FileNotFoundError:
            return None

    def __str__(self):
        return self.user.username
    
    
class DoctorModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    nid = models.IntegerField(unique=True)
    phone_number = models.CharField(max_length=15, validators=[validate_phone_number])
    city = models.CharField(max_length=20)
    street_address = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    specialization = models.CharField(max_length=50, choices=VACCINE_SPECIALIZATIONS)
    license_number = models.CharField(max_length=8, validators=[validate_license_number],unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE, default='doctor')
    user_photo = models.ImageField(upload_to='images/user/', blank=True,null=True)
    is_valid = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.user_photo:
            self.user_photo = self.get_default_photo(self.gender)
        super().save(*args, **kwargs)
    
    def get_default_photo(self, gender):
        if gender == 'male':
            default_image_path = 'images/user/male_default.png'
        elif gender == 'female':
            default_image_path = 'images/user/female_default.png'
        else:
            default_image_path = 'images/user/default_user.png'
        
        try:
            with open(default_image_path, 'rb') as image_file:
                return ContentFile(image_file.read(), 'default_photo.jpg')
        except FileNotFoundError:
            return None

    def __str__(self):
        return f"Dr. {self.user.username}"