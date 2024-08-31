from django.core.exceptions import ValidationError
import random
from django.apps import apps
def generate_unique_patient_number():
    PatientModel = apps.get_model('app_user', 'PatientModel')
    while True:
        number = f"{random.randint(100000,999999)}"
        if not PatientModel.objects.filter(patient_id=number).exists():
            return number
        
def validate_nid(value):
    if len(str(value)) != 10:  # Example check for a 10-digit NID
        raise ValidationError('NID must be 10 digits long.')
    
def validate_phone_number(value):
    if len(value) < 11 or len(value) > 14:  # Check for reasonable phone number length
        raise ValidationError('Phone number must be between 10 and 15 digits.')
    
def validate_license_number(value):
    if len(str(value)) != 8 or not str(value).isdigit():
        raise ValidationError('License number must be exactly 8 digits.')