from django.db import models


class WeatherCity(models.Model):
    """The city shown in the sidebar Weather widget. Only one should be
    marked default; live temperature is fetched from OpenWeatherMap using
    these coordinates (falls back to `manual_*` fields if no API key is set)."""
    city_name_hi = models.CharField(max_length=100)
    city_name_en = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_default = models.BooleanField(default=False, help_text="Only one city can be default — marking this one automatically un-marks any other.")

    # Manual fallback values, editable from admin, used when no WEATHER_API_KEY is configured.
    manual_temp_c = models.DecimalField(max_digits=4, decimal_places=1, default=28.0)
    manual_condition_hi = models.CharField(max_length=100, default="साफ आसमान")
    manual_condition_en = models.CharField(max_length=100, default="Clear Sky")
    manual_humidity = models.PositiveIntegerField(default=45)
    manual_wind_kmh = models.DecimalField(max_digits=5, decimal_places=1, default=10.0)

    def __str__(self):
        return self.city_name_en

    def save(self, *args, **kwargs):
        # Enforce a single default city — marking this one default silently
        # un-marks any previous default, so the widget never has to guess
        # which of several "default" rows to show.
        if self.is_default:
            WeatherCity.objects.exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
