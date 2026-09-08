from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_current_weather
from .serializers import WeatherSerializer


class CurrentWeatherView(APIView):
    """GET /api/v1/weather/current/ — live (or manual-fallback) weather for the sidebar widget."""

    def get(self, request):
        data = get_current_weather()
        if not data:
            return Response({"detail": "No weather city configured."}, status=404)
        return Response(WeatherSerializer(data).data)
