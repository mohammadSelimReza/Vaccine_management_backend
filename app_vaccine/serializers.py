from rest_framework import serializers
from .models import VaccineModel,VaccineCampaignModel,BookingModel,BookingCampaignModel,VaccineTypeModel,Comment
from datetime import date
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from app_user.models import PatientModel
from django.contrib.auth.models import User
class VaccineSerializer(serializers.ModelSerializer):
    # added_by =serializers.CharField(source='added_by.name',)
    class Meta:
        model = VaccineModel
        fields = '__all__'
        
    def validate_added_by(self, value):
        if not value.is_valid:
            raise serializers.ValidationError("Only verified doctors can add vaccines.")
        return value

class VaccineCampaignSerializer(serializers.ModelSerializer):
    campaign_vaccine_name = serializers.CharField(source='campaign_vaccine.name', read_only=True)
    added_by_name = serializers.CharField(source='added_by.name', read_only=True)
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
        fields = ['user','patient_name', 'patient_age', 'vaccine', 'first_dose_date', 'dose_dates']
        read_only_fields = ['dose_dates']

    def validate_first_dose_date(self, value):
        if value < date.today():
            raise ValidationError("The date cannot be in the past.")
        return value
    
class BookCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingCampaignModel
        fields = ['user', 'patient_name', 'patient_age', 'campaign_name', 'booked_date']

    def validate_booked_date(self, value):
        if value < date.today():
            raise ValidationError("The date cannot be in the past.")
        return value

    def create(self, validated_data):
        validated_data['is_booked'] = True
        return super().create(validated_data)
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['patient_name','patient_img', 'campaign', 'text']

    def validate(self, data):
        user = self.context['request'].user
        patient_name = data['patient_name']
        campaign = data['campaign']

        # Check if the patient has booked this campaign
        booking = BookingCampaignModel.objects.filter(patient_name=patient_name, campaign_name=campaign, is_booked=True).first()
        if not booking:
            raise serializers.ValidationError("You can only comment if you have booked this campaign.")
        
        return data


class VaccineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineTypeModel
        fields = '__all__'