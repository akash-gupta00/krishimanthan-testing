from rest_framework import viewsets
from django.utils import timezone
from .models import EPaperIssue
from .serializers import EPaperIssueSerializer

MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}


class EPaperIssueViewSet(viewsets.ReadOnlyModelViewSet):
    """Latest issue is first (ordering = -issue_date). Frontend uses list[0] as "today's" issue."""
    serializer_class = EPaperIssueSerializer

    def get_queryset(self):
        today = timezone.localdate()
        
        # Sirf published aur aaj ya aaj se purani date ke papers aayenge (future dates block)
        queryset = EPaperIssue.objects.filter(
            is_published=True,
            issue_date__lte=today
        )

        # Year aur Month query params agar frontend filter kare (?year=2026&month=September)
        year = self.request.query_params.get("year")
        month = self.request.query_params.get("month")

        if year and year.isdigit():
            queryset = queryset.filter(issue_date__year=int(year))

        if month:
            val_str = str(month).strip().lower()
            if val_str.isdigit():
                queryset = queryset.filter(issue_date__month=int(val_str))
            elif val_str in MONTH_MAP:
                queryset = queryset.filter(issue_date__month=MONTH_MAP[val_str])

        return queryset.order_by("-issue_date")