from django.contrib import admin

from operation.models import Operation, BuyData, SellData

admin.site.register(Operation)
admin.site.register(BuyData)
admin.site.register(SellData)
# Register your models here.
