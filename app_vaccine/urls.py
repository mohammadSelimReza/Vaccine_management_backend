from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'list',views.VaccineView,basename='vaccineList')
router.register(r'campaign',views.CampaignView,basename='campaignList')
router.register(r'book-vaccine', views.BookVaccineViewSet, basename='book-vaccine')
router.register(r'book-campaign', views.BookCampaignViewSet, basename='book-campaign')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'vaccine-type', views.TypeViewSet, basename='type')
urlpatterns = [
    path('', include(router.urls)),
    # Directly add the ListCreateAPIView to the urlpatterns
    path('add/', views.VaccineListCreateAPIView.as_view(), name='add-vaccine'),
    path('campaign-add/', views.VaccineCampaignListCreateAPIView.as_view(), name='add-campaign'),
    path('edit/<pk>/',views.EditVaccineView.as_view(), name='edit-campaign'),
    path('delete/<int:pk>/',views.VaccineDeleteView.as_view(), name='deleteVaccine'),
    path('total-vaccines/', views.TotalVaccineView.as_view(), name='total_vaccines_count'),
    path('total-campaigns/', views.TotalCampaignView.as_view(), name='total_campaigns_count'),
    path('total-campaigns-book/', views.TotalBookedOnCampaignView.as_view(), name='total_campaigns_book_count'),
    
]
