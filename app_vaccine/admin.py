from django.contrib import admin
from .models import TotalBookedOnCampaign,TotalVaccineModel,TotalCampaignAdded,VaccineModel,VaccineCampaignModel,VaccineTypeModel,BookingCampaignModel,Comment
# Register your models here.
class VaccineModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('vaccine_name',)}
class VaccineCampaignModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('campaign_name',)}
admin.site.register(VaccineModel,VaccineModelAdmin)
admin.site.register(VaccineCampaignModel,VaccineCampaignModelAdmin)
admin.site.register(VaccineTypeModel)
admin.site.register(BookingCampaignModel)
admin.site.register(Comment)
admin.site.register(TotalVaccineModel)
admin.site.register(TotalCampaignAdded)
admin.site.register(TotalBookedOnCampaign)
