from rest_framework import viewsets,generics,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import PatientModel,DoctorModel
from .serializers import UserSerializer,UserPasswordUpdateSerializer,PatientRegistrationSerializer,DoctorRegistrationSerializer,LoginSerializer,UserNameUpdateSerializer,PatientProfileUpdateSerializer,DoctorProfileUpdateSerializer
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import redirect
from  django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = PatientModel.objects.all()
    serializer_class = PatientRegistrationSerializer
    permission_classes = [AllowAny]

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = DoctorModel.objects.all()
    serializer_class = DoctorRegistrationSerializer
    permission_classes = [AllowAny]
    
    
    

class PatientRegistrationViewSet(generics.CreateAPIView):
    queryset = PatientModel.objects.all()
    serializer_class = PatientRegistrationSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()  # `patient` is the PatientModel instance
            user = patient.user  # Access the associated User instance
            
            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Prepare the confirmation email
            confirm_link = f"http://127.0.0.1:8000/user/activate/{uid}/{token}"
            email_subject = "Confirm your email"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            # Send the email
            email.send()

            return Response({"detail": "Check your email to confirm your account"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorRegistrationViewSet(APIView):
    queryset = DoctorModel.objects.all()
    serializer_class = DoctorRegistrationSerializer
    permission_classes= [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()  # `patient` is the PatientModel instance
            user = patient.user  # Access the associated User instance
            
            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Prepare the confirmation email
            confirm_link = f"https://vaccine-management-backend-phvj.onrender.com/user/activate/{uid}/{token}"
            email_subject = "Confirm your email"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            # Send the email
            email.send()

            return Response({"detail": "Check your email to confirm your account"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('https://vaccine-hub.netlify.app')
    
    return redirect('patientRegistration')
      

    
class LoginSerializerView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = LoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                token,_ = Token.objects.get_or_create(user=user)
                login(request,user)
                return Response({'token':token.key,'user.id':user.id})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
            
class LogoutView(APIView):
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('https://vaccine-hub.netlify.app/')
    
    
class UserNameUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]  
    queryset = User.objects.all()
    serializer_class = UserNameUpdateSerializer

    def get_object(self):
        # Return the current authenticated user
        return self.request.user
    
class UserPasswordUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserPasswordUpdateSerializer
    queryset = User.objects.all()
    def get_object(self):
        return self.request.user
    
class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        print(user)
        
        if hasattr(user,'patients') and user.patients.user_type == 'Patient':
            return PatientModel.objects.all()
        elif hasattr(user,'doctor') and user.doctor.user_type == 'Doctor':
            return DoctorModel.objects.all()
        else:
            return None
    def get_serializer_class(self):
        user = self.request.user
        if hasattr(user, 'patients') and user.patients.user_type == 'Patient':
            # If the user is a patient, use PatientProfileUpdateSerializer
            return PatientProfileUpdateSerializer
        elif hasattr(user, 'doctor') and user.doctor.user_type == 'Doctor':
            # If the user is a doctor, use DoctorProfileUpdateSerializer
            return DoctorProfileUpdateSerializer
        else:
            return None
    def get_object(self):
        # Use the get_queryset method to fetch the correct object
        queryset = self.get_queryset()
        if queryset is not None:
            return queryset.first()  # Get the first and only object in the queryset
        else:
            raise Response(
                {"detail": "User type not recognized or you do not have permission to access this profile."},
                status=status.HTTP_403_FORBIDDEN
            )