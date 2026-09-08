from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SiteSettings
from .serializers import SiteSettingsSerializer


class SiteSettingsView(APIView):
    """GET /api/v1/site-settings/ — global site identity/contact/social/SEO defaults."""

    def get(self, request):
        return Response(SiteSettingsSerializer(SiteSettings.load(), context={"request": request}).data)
