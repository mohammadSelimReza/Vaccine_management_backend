from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PatientModel,DoctorModel
from .constants import GENDER_TYPE, USER_TYPE
from .validators import generate_unique_patient_number
from django.contrib.auth.hashers import make_password
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email', 'password', 'password2']
        extra_kwargs = {"password":{"write_only": True},"password2":{"write_only": True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user

class PatientRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    user_type = serializers.CharField(read_only=True, default='patient')
    class Meta:
        model = PatientModel
        fields = [
            'user', 'birth_date', 'gender', 'nid', 'phone_number', 'city',
            'street_address', 'zip_code', 'user_type', 'user_photo'
        ]
        extra_kwargs = {
            'user_photo': {'required': False, 'allow_null': True},
        }
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        
        patient = PatientModel(
            user=user,
            birth_date=validated_data['birth_date'],
            gender=validated_data['gender'],
            nid=validated_data['nid'],
            phone_number=validated_data['phone_number'],
            city=validated_data['city'],
            street_address=validated_data['street_address'],
            zip_code=validated_data['zip_code'],
            user_type='patient',
            user_photo=validated_data.get('user_photo', None),
            patient_id=generate_unique_patient_number()
        )
        patient.save()
        return patient

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    user_type = serializers.CharField(read_only=True, default='doctor')
    class Meta:
        model = DoctorModel
        fields = [
                 'user', 'birth_date', 'gender', 'nid', 'phone_number', 'city',
                'street_address', 'zip_code', 'specialization', 'license_number',
                'user_type', 'user_photo'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        
        doctor = DoctorModel(
            user=user,
            birth_date=validated_data['birth_date'],
            gender=validated_data['gender'],
            nid=validated_data['nid'],
            phone_number=validated_data['phone_number'],
            city=validated_data['city'],
            street_address=validated_data['street_address'],
            zip_code=validated_data['zip_code'],
            specialization=validated_data['specialization'],
            license_number=validated_data['license_number'],
            user_type='doctor',
            user_photo=validated_data.get('user_photo', None)
        )
        doctor.save()
        return doctor
    
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20,style={'input_type': 'text'})
    password = serializers.CharField(max_length=64, style={'input_type': 'password'})
    
class UserNameUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50,style={'input_type':'text'})
    last_name = serializers.CharField(max_length=50,style={'input_type':'text'})
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['password', 'password2']
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['password'])
        instance.save()
        return instance
class PatientProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientModel
        fields = ['birth_date', 'gender', 'nid', 'phone_number', 'city', 'street_address', 'zip_code', 'user_photo']
        
class DoctorProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorModel
        fields = ['birth_date', 'gender', 'nid', 'phone_number', 'city', 'street_address', 'zip_code', 'specialization', 'license_number', 'user_photo']