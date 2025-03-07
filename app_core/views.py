from rest_framework.viewsets import  ModelViewSet
from rest_framework.permissions import AllowAny
from . import models
from .serializers import BannerSerializer,TestimonialSerializer

# Create your views here.
class BannerView(ModelViewSet):
    queryset = models.BannerModel.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [AllowAny]

class TestimonialView(ModelViewSet):
    queryset = models.TestimonialModel.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]