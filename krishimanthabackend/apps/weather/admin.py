from django.contrib import admin
from .models import WeatherCity


@admin.register(WeatherCity)
class WeatherCityAdmin(admin.ModelAdmin):
    list_display = ("city_name_en", "is_default", "manual_temp_c", "manual_condition_en")
    list_editable = ("is_default",)
