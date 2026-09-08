from rest_framework import viewsets, mixins
from django.db.models import Q
from django.utils import timezone
from .models import Advertisement, AdSlot
from .serializers import ActiveAdSerializer, AdSubmissionSerializer, AdSlotSerializer


class AdSlotViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/ads/slots/ — lets the frontend 'Post Your Ads' form list valid slot keys."""
    queryset = AdSlot.objects.all()
    serializer_class = AdSlotSerializer
    lookup_field = "key"


class ActiveAdViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/ads/?slot=<key> — currently-approved, in-date ads for a slot."""
    serializer_class = ActiveAdSerializer

    def get_queryset(self):
        today = timezone.localdate()
        qs = Advertisement.objects.filter(status=Advertisement.Status.APPROVED).select_related("slot")
        qs = qs.filter(
            (Q(start_date__isnull=True) | Q(start_date__lte=today))
            & (Q(end_date__isnull=True) | Q(end_date__gte=today))
        )

        # Handle different param names (?slot=, ?placement=, ?position=)
        slot_param = (
            self.request.query_params.get("slot")
            or self.request.query_params.get("placement")
            or self.request.query_params.get("position")
        )

        if slot_param:
            raw_key = slot_param.strip()
            # Normalize: "sidebar_top" and "sidebar-top" both match
            alt_key1 = raw_key.replace("_", "-")
            alt_key2 = raw_key.replace("-", "_")

            qs = qs.filter(
                Q(slot__key__iexact=raw_key)
                | Q(slot__key__iexact=alt_key1)
                | Q(slot__key__iexact=alt_key2)
                | Q(slot__name__iexact=raw_key)
            )

        return qs.order_by("-created_at")


class AdSubmissionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """POST /api/v1/ads/submit/ — public 'Post Your Ads' form handler."""
    queryset = Advertisement.objects.all()
    serializer_class = AdSubmissionSerializer