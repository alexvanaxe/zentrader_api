from django.contrib import admin

# Register your models here.
from stock.models import Stock

admin.site.register(Stock)
