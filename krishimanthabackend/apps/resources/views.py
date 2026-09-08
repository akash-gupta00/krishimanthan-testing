from rest_framework import viewsets
from .models import Resource
from .serializers import ResourceSerializer


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Resource.objects.filter(is_published=True)
    serializer_class = ResourceSerializer
