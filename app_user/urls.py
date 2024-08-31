from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
router = DefaultRouter()
router.register(r'patients', views.PatientViewSet)
router.register(r'doctors', views.DoctorViewSet)
router.register(r'users', views.UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('patient/registration/',views.PatientRegistrationViewSet.as_view(),name='patientRegistration'),
    path('doctor/registration/',views.DoctorRegistrationViewSet.as_view(),name='doctorRegistration'),
    path('activate/<uid64>/<token>/',views.activate,name='activate'),
    path('login/',views.LoginSerializerView.as_view(),name='login'),

    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('update-name/', views.UserNameUpdateView.as_view(), name='userName'),
    path('update-profile/',views.UserProfileUpdateView.as_view(),name='userProfile'),
    path('api/token/',TokenObtainPairView.as_view(),name='apiToken'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='apiTokenRefresh'),
    path('update-password/', views.UserPasswordUpdateView.as_view(), name='update-password'),
]
