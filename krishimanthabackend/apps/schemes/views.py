from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from django.db.models import Q
from .models import Scheme
from .serializers import SchemeSerializer


class SchemeFilter(filters.FilterSet):
    department = filters.CharFilter(method="filter_by_department")
    dept = filters.CharFilter(method="filter_by_department")

    class Meta:
        model = Scheme
        fields = ["department", "dept"]

    def filter_by_department(self, queryset, name, value):
        if not value:
            return queryset
        val = str(value).strip()
        # Agar number pass ho (?department=1)
        if val.isdigit():
            return queryset.filter(department_id=int(val))
        # Agar slug ya Hindi/English naam pass ho (?department=agriculture)
        return queryset.filter(
            Q(department__slug__iexact=val) |
            Q(department__name_en__iexact=val) |
            Q(department__name_hi__iexact=val)
        )


class SchemeViewSet(viewsets.ReadOnlyModelViewSet):
    """Public government-schemes list/detail API. ?department=<slug|id> &search=<text>"""
    queryset = Scheme.objects.filter(is_published=True).select_related("department")
    serializer_class = SchemeSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    filterset_class = SchemeFilter
    search_fields = ["name_hi", "name_en", "overview_hi", "overview_en"]
    lookup_field = "slug"