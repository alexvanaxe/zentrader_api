from django.contrib import admin

from operation.models import Operation, ExperienceData, BuyData, SellData

admin.site.register(Operation)
admin.site.register(ExperienceData)
admin.site.register(BuyData)
admin.site.register(SellData)
# Register your models here.
