from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.
class BannerModel(models.Model):
    title = models.CharField(max_length=100)
    banner_img = CloudinaryField('banner_img', blank=True, null=True)