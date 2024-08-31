from rest_framework import serializers
from .models import BannerModel
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerModel
        fields = '__all__'