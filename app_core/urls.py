from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'details',views.BannerView,basename='banner_view')
router.register(r'testimonial',views.TestimonialView,basename='testimonial_view')
urlpatterns = [
    path('', include(router.urls)),
]