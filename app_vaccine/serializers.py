from rest_framework import serializers
from .models import VaccineModel,VaccineCampaignModel,BookingModel,BookingCampaignModel,VaccineTypeModel,Comment
from datetime import date
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from app_user.models import PatientModel
class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineModel
        fields = '__all__'
        
    def validate_added_by(self, value):
        if not value.is_valid:
            raise serializers.ValidationError("Only verified doctors can add vaccines.")
        return value

class VaccineCampaignSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = VaccineCampaignModel
        fields = '__all__'
        
    def validate_added_by(self, value):
        if not value.is_valid:
            raise serializers.ValidationError("Only verified doctors can add vaccines.")
        return value
    
class BookVaccineSerializer(serializers.ModelSerializer):
    first_dose_date = serializers.DateField(format='%Y-%m-%d')

    class Meta:
        model = BookingModel
        fields = ['patient_name', 'patient_age', 'vaccine', 'first_dose_date', 'dose_dates']
        read_only_fields = ['dose_dates']

    def validate_first_dose_date(self, value):
        if value < date.today():
            raise ValidationError("The date cannot be in the past.")
        return value
    
class BookCampaignSerializer(serializers.ModelSerializer):
    first_dose_date = serializers.DateField(format='%Y-%m-%d')

    class Meta:
        model = BookingCampaignModel
        # fields = ['patient_name','patient_age','campaign_name','book_date']
        fields = '__all__'
    def validate_first_dose_date(self, value):
        if value < date.today():
            raise ValidationError("The date cannot be in the past.")
        return value
    def create(self,validated_data):
        validated_data['is_booked'] = True
        return super().create(validated_data)
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['patient_name','campaign','text']

    def validate(self, data):
        user = self.context['request'].user
        patient = get_object_or_404(PatientModel, user=user)
        campaign = data['campaign']

        # Check if the patient has booked this campaign
        booking = BookingCampaignModel.objects.filter(patient=patient, campaign_name=campaign, is_booked=True).first()
        if not booking:
            raise serializers.ValidationError("You can only comment if you have booked this campaign.")
        
        return data
    def create(self, validated_data):
        user = self.context['request'].user
        patient = get_object_or_404(PatientModel, user=user)
        validated_data['patient'] = patient
        return super().create(validated_data)

# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ['patient','patient_name', 'campaign', 'text', 'created_at']
#         read_only_fields = ['created_at']

#     def create(self, validated_data):
#             user = self.context['request'].user
#             patient = get_object_or_404(PatientModel, user=user)
#             validated_data['patient'] = patient
            
#             booking = get_object_or_404(
#                 BookingCampaignModel,
#                 patient_name=patient,
#                 campaign_name=validated_data['campaign'],
#                 is_booked=True
#             )
            
#             if not booking.is_booked:
#                 raise ValidationError("You must have a confirmed booking to comment on this campaign.")
            
#             return super().create(validated_data)

class VaccineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineTypeModel
        fields = '__all__'