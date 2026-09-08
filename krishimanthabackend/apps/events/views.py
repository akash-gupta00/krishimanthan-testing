from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django.utils import timezone
from .models import Event
from .serializers import EventSerializer

MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public events list/detail API.
    ?upcoming=true|false filters by whether event_date is in the future.
    ?year=2026 &month=July / &month=7
    """
    queryset = Event.objects.filter(is_published=True)
    serializer_class = EventSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title_hi", "title_en", "location_hi", "location_en"]
    lookup_field = "slug"

    def get_queryset(self):
        qs = super().get_queryset()
        upcoming = self.request.query_params.get("upcoming")
        year = self.request.query_params.get("year")
        month = self.request.query_params.get("month")
        today = timezone.localdate()

        if upcoming == "true":
            qs = qs.filter(event_date__gte=today)
        elif upcoming == "false":
            qs = qs.filter(event_date__lt=today)

        # Year filtering
        if year and year.isdigit():
            qs = qs.filter(event_date__year=int(year))

        # Month filtering (handles "July" or "7")
        if month:
            val_str = str(month).strip().lower()
            if val_str.isdigit():
                qs = qs.filter(event_date__month=int(val_str))
            elif val_str in MONTH_MAP:
                qs = qs.filter(event_date__month=MONTH_MAP[val_str])

        return qs.order_by("-event_date")