from rest_framework import viewsets
from .models import MarketPrice
from .serializers import MarketPriceSerializer


class MarketPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MarketPrice.objects.filter(is_published=True)
    serializer_class = MarketPriceSerializer
