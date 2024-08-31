from rest_framework import serializers
from .models import VaccineModel,VaccineCampaignModel,BookingModel,BookingCampaignModel,Comment
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
        fields = ['patient_name', 'patient_age', 'campaign_name', 'first_dose_date', 'dose_dates']
        read_only_fields = ['dose_dates']

    def validate_first_dose_date(self, value):
        if value < date.today():
            raise ValidationError("The date cannot be in the past.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['patient','patient_name', 'campaign', 'text', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        patient = get_object_or_404(PatientModel, user=user)
        validated_data['patient'] = patient
        return super().create(validated_data)
