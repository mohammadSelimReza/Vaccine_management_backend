from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.
class BannerModel(models.Model):
    title = models.CharField(max_length=100)
    banner_img = CloudinaryField('banner_img', blank=True, null=True)

class TestimonialModel(models.Model):
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=255)
    def __str__(self):
        return f"Testimonial by {self.name}"