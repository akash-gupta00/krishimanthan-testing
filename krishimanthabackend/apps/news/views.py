from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from .models import NewsItem, NewsCategory
from .serializers import NewsItemListSerializer, NewsItemDetailSerializer, NewsCategorySerializer

MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}

class NewsItemFilter(filters.FilterSet):
    """Exposes clean query params (?category=<slug>&department=<slug>&year=2026&month=2)"""
    category = filters.CharFilter(field_name="category__slug")
    department = filters.CharFilter(field_name="department__slug")
    year = filters.NumberFilter(field_name="published_date__year")
    month = filters.CharFilter(method="filter_by_month")

    class Meta:
        model = NewsItem
        fields = ["category", "department", "year", "month"]

    def filter_by_month(self, queryset, name, value):
        if not value:
            return queryset
        val_str = str(value).strip().lower()
        if val_str.isdigit():
            return queryset.filter(published_date__month=int(val_str))
        if val_str in MONTH_MAP:
            return queryset.filter(published_date__month=MONTH_MAP[val_str])
        return queryset


class NewsCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer


class NewsItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public news list/detail API.
    Only shows news published on or before today.
    """
    serializer_class = NewsItemListSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NewsItemFilter
    search_fields = ["title_hi", "title_en", "summary_hi", "summary_en"]
    ordering_fields = ["published_date", "created_at"]
    ordering = ["-published_date"]
    lookup_field = "slug"

    def get_queryset(self):
        today = timezone.localdate()
        return NewsItem.objects.filter(
            is_published=True,
            published_date__lte=today
        ).select_related("category", "department")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return NewsItemDetailSerializer
        return NewsItemListSerializer