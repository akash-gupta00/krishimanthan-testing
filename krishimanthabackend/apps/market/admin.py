from django.contrib import admin
from .models import MarketPrice


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ("crop_name_en", "price", "unit_en", "trend", "order", "is_published")
    list_editable = ("price", "trend", "order", "is_published")
