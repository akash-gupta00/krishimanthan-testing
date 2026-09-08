from rest_framework import viewsets
from django.utils import timezone
from django.db.models import Q
from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    """?placement=ticker|sidebar filters which widget's announcements to return."""
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        today = timezone.localdate()
        qs = Announcement.objects.filter(is_published=True).filter(
            (Q(start_date__isnull=True) | Q(start_date__lte=today))
            & (Q(end_date__isnull=True) | Q(end_date__gte=today))
        )
        placement = self.request.query_params.get("placement")
        if placement == "ticker":
            qs = qs.filter(show_in_ticker=True)
        elif placement == "sidebar":
            qs = qs.filter(show_in_sidebar=True)
        return qs
