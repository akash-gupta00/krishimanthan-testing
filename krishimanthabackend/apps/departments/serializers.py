from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name_hi", "name_en", "slug", "description_hi", "description_en", "icon", "color_tone", "order"]
