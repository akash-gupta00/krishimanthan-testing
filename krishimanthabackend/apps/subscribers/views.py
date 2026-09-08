from rest_framework import mixins, viewsets
from .models import Subscriber
from .serializers import SubscriberSerializer


class SubscriberViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """POST /api/v1/subscribers/ — Subscribe page + footer newsletter + top-bar modal all post here."""
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
