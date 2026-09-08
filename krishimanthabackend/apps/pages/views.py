from rest_framework import viewsets
from .models import StaticPage
from .serializers import StaticPageSerializer


class StaticPageViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/pages/<slug>/ — e.g. /api/v1/pages/privacy-policy/"""
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageSerializer
    lookup_field = "slug"
