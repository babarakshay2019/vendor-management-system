from django.contrib import admin
from .models import Vendor, HistoricalPerformance

admin.site.register((Vendor, HistoricalPerformance))
