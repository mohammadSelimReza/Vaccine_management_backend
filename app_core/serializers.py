from rest_framework import serializers
from .models import BannerModel,TestimonialModel
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerModel
        fields = '__all__'
        
class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestimonialModel
        fields = '__all__'
        