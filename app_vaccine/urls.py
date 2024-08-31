from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'list',views.VaccineView,basename='vaccineList')
router.register(r'campaign',views.CampaignView,basename='campaignList')
router.register(r'book-vaccine', views.BookVaccineViewSet, basename='book-vaccine')
router.register(r'book-campaign', views.BookCampaignViewSet, basename='book-campaign')
router.register(r'comments', views.CommentViewSet, basename='comment')
urlpatterns = [
    path('', include(router.urls)),
    # Directly add the ListCreateAPIView to the urlpatterns
    path('add/', views.VaccineListCreateAPIView.as_view(), name='add-vaccine'),
    path('add/campaign/', views.VaccineCampaignListCreateAPIView.as_view(), name='add-campaign'),
    path('edit/<pk>/',views.EditVaccineView.as_view(), name='edit-campaign'),
    path('delete/<int:pk>/',views.VaccineDeleteView.as_view(), name='deleteVaccine'),
]
