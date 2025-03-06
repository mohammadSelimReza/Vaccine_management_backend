from rest_framework import generics,serializers,status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import TotalBookedOnCampaign,TotalVaccineModel,TotalCampaignAdded,VaccineModel,VaccineCampaignModel,BookingModel,BookingCampaignModel,Comment,VaccineTypeModel
from .serializers import  VaccineTypeSerializer,VaccineSerializer,VaccineCampaignSerializer,BookVaccineSerializer,BookCampaignSerializer,CommentSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from app_user.models import PatientModel
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class VaccineView(ModelViewSet):
    queryset = VaccineModel.objects.all()
    serializer_class = VaccineSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['vaccine_for']
    ordering_fields = ['vaccine_name', 'expiration_date']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Handle filtering by 'vaccine_for'
        vaccine_filtering = self.request.query_params.get('type', None)
        if vaccine_filtering and vaccine_filtering.lower() != "none":
            queryset = queryset.filter(vaccine_for=vaccine_filtering)

        # Handle ordering, apply ordering only if it's valid
        ordering = self.request.query_params.get('ordering', None)
        if ordering and ordering in self.ordering_fields:
            queryset = queryset.order_by(ordering)

        return queryset



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
        
        # Ensure the doctor is verified before proceeding
        if not doctor.is_valid:
            raise ValidationError("Only verified doctors can add vaccines.")
        
        # Fetch or create the TotalVaccineModel instance
        total_count, created = TotalVaccineModel.objects.get_or_create(id=1)
        
        # Increment the total vaccine count and save
        total_count.total_vaccine += 1
        total_count.save()

        # Save the vaccine entry with the associated doctor
        serializer.save(added_by=doctor)
        
        # Log or print debug info
        print(f"Total vaccines updated: {total_count.total_vaccine}")

class VaccineDetailAPIView(generics.RetrieveAPIView):
    queryset = VaccineModel.objects.all()
    serializer_class = VaccineSerializer
    permission_classes = [AllowAny]
        
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
        total_count,created=TotalCampaignAdded.objects.get_or_create(id=1)
        total_count.total_campaign += 1
        total_count.campaign_target += serializer.validated_data['target_population']
        total_count.save()
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
    serializer_class = BookCampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Add logging to check if user is correctly retrieved
        total_count,created= TotalBookedOnCampaign.objects.get_or_create(id=1)
        total_count.total_booked += 1
        total_count.save()
        print(f"Request user: {user}")
        return BookingCampaignModel.objects.filter(user=user.id)
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            # Log the exception
            print(f"Error: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
    
    
class TotalVaccineView(APIView):
    queryset = TotalVaccineModel.objects.all()
    def get(self, request):
            try:
                # Fetch the total vaccine count for id=1
                total_vaccines = TotalVaccineModel.objects.get(id=1)
                count = total_vaccines.total_vaccine
            except TotalVaccineModel.DoesNotExist:
                count = 0
            
            return Response({"total_vaccine": count})
class TotalCampaignView(APIView):
    queryset = TotalCampaignAdded.objects.all()
    def get(self,request):
        total_campaigns = TotalCampaignAdded.objects.get(id=1)
        count = total_campaigns.total_campaign if total_campaigns else 0
        target_count = total_campaigns.campaign_target if total_campaigns else 0
        return Response({"total_campaign": count,"target_count":target_count})
class TotalBookedOnCampaignView(APIView):
    queryset = TotalBookedOnCampaign.objects.all()
    def get(self,request):
        total_campaigns = TotalBookedOnCampaign.objects.get(id=1)
        count = total_campaigns.total_booked if total_campaigns else 0
        return Response({"total_booked": count})