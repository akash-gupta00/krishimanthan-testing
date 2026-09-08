from rest_framework import viewsets
from .models import Department
from .serializers import DepartmentSerializer


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """Public read-only list of departments (Agriculture, Cooperation, Panchayat, Forest, Animal Husbandry)."""
    queryset = Department.objects.filter(is_published=True)
    serializer_class = DepartmentSerializer
    lookup_field = "slug"
