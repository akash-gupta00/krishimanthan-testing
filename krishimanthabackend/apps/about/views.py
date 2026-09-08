from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AboutContent
from .serializers import AboutContentSerializer


class AboutContentView(APIView):
    """GET /api/v1/about/ — intro text + the 3 highlight cards, in one call."""

    def get(self, request):
        return Response(AboutContentSerializer(AboutContent.load()).data)
