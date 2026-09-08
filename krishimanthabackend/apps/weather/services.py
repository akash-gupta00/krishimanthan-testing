import requests
from django.conf import settings
from django.core.cache import cache
from .models import WeatherCity


def get_current_weather():
    """
    Returns live weather for the default city if WEATHER_API_KEY is set
    (OpenWeatherMap One Call / Current Weather API), cached for 30 minutes
    to stay well within free-tier rate limits. Falls back to the manually
    entered values on the WeatherCity record if no key is configured or
    the request fails — the sidebar widget never breaks either way.
    """
    city = WeatherCity.objects.filter(is_default=True).first()
    if not city:
        city = WeatherCity.objects.first()
    if not city:
        return None

    cache_key = f"weather:{city.id}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    result = {
        "city_hi": city.city_name_hi,
        "city_en": city.city_name_en,
        "temp_c": float(city.manual_temp_c),
        "condition_hi": city.manual_condition_hi,
        "condition_en": city.manual_condition_en,
        "humidity": city.manual_humidity,
        "wind_kmh": float(city.manual_wind_kmh),
        "source": "manual",
    }

    if settings.WEATHER_API_KEY:
        try:
            resp = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "lat": city.latitude,
                    "lon": city.longitude,
                    "appid": settings.WEATHER_API_KEY,
                    "units": "metric",
                },
                timeout=5,
            )
            if resp.ok:
                data = resp.json()
                result.update({
                    "temp_c": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "wind_kmh": round(data["wind"]["speed"] * 3.6, 1),
                    "condition_en": data["weather"][0]["description"].title(),
                    "source": "openweathermap",
                })
        except Exception:
            pass  # keep manual fallback — a network hiccup should never break the widget

    cache.set(cache_key, result, 60 * 30)
    return result
