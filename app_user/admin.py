from django.contrib import admin
from .models import PatientModel,DoctorModel,TotalPatientsModel
# Register your models here.

admin.site.register(PatientModel)
admin.site.register(DoctorModel)
admin.site.register(TotalPatientsModel)