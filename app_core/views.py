from django.shortcuts import render
from .models import BannerModel
from .serializers import BannerSerializer
from rest_framework.viewsets import  ModelViewSet
from rest_framework.permissions import AllowAny

# Create your views here.
class BannerView(ModelViewSet):
    queryset = BannerModel.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [AllowAny]
