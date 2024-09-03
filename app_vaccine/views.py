from rest_framework import generics,serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import VaccineModel,VaccineCampaignModel,BookingModel,BookingCampaignModel,Comment,VaccineTypeModel
from .serializers import  VaccineTypeSerializer,VaccineSerializer,VaccineCampaignSerializer,BookVaccineSerializer,BookCampaignSerializer,CommentSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from app_user.models import PatientModel
class VaccineView(ModelViewSet):
    queryset = VaccineModel.objects.all()
    serializer_class = VaccineSerializer
    permission_classes = [AllowAny]

class CampaignView(ModelViewSet):
    queryset = VaccineCampaignModel.objects.all()
    serializer_class = VaccineCampaignSerializer
    permission_classes = [AllowAny]

class VaccineListCreateAPIView(generics.ListCreateAPIView):
    queryset = VaccineModel.objects.all()
    serializer_class = VaccineSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        doctor = self.request.user.doctor
        if not doctor.is_valid:
            raise ValidationError("Only verified doctors can add vaccines.")
        serializer.save(added_by=doctor)
        
class EditVaccineView(generics.RetrieveUpdateAPIView):
    queryset = VaccineModel.objects.all()
    serializer_class = VaccineSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        doctor = self.request.user.doctor
        if not doctor.is_valid:
            raise ValidationError("Only verified doctors can add vaccines.")
        serializer.save(added_by=doctor)

class VaccineDeleteView(generics.DestroyAPIView):
    queryset = VaccineModel.objects.all()
    serializer_class = VaccineSerializer
    permission_classes = [IsAuthenticated]


class VaccineCampaignListCreateAPIView(generics.ListCreateAPIView):
    queryset = VaccineCampaignModel.objects.all()
    serializer_class = VaccineCampaignSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        doctor = self.request.user.doctor
        if not doctor.is_valid:
            raise serializers.ValidationError("Only verified doctors can create vaccine campaigns.")
        serializer.save(added_by=doctor)
        
class BookVaccineViewSet(ModelViewSet):
    queryset = BookingModel.objects.all()
    serializer_class = BookVaccineSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save()  # Or handle patient information as needed
        else:
            raise PermissionDenied("You must be logged in to book a vaccine.")

class BookCampaignViewSet(ModelViewSet):
    queryset = BookingCampaignModel.objects.all()
    serializer_class = BookCampaignSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        
        
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        user = self.request.user
        patient = get_object_or_404(PatientModel, user=user)
        serializer.save(patient=patient)
        
class TypeViewSet(ModelViewSet):
    queryset = VaccineTypeModel.objects.all()
    serializer_class = VaccineTypeSerializer
    permission_classes = [AllowAny]