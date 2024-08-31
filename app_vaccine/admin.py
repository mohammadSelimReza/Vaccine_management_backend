from django.contrib import admin
from .models import VaccineModel,VaccineCampaignModel
# Register your models here.
class VaccineModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('vaccine_name',)}
class VaccineCampaignModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('campaign_name',)}
admin.site.register(VaccineModel,VaccineModelAdmin)
admin.site.register(VaccineCampaignModel,VaccineCampaignModelAdmin)

