from django.db import models

# Create your models here.
class BannerModel(models.Model):
    title = models.CharField(max_length=100)
    banner_img = models.ImageField(upload_to='images/banner/', blank=True,null=True)