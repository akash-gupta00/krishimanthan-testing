from rest_framework import serializers
from .models import Scheme


class SchemeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    department_slug = serializers.SlugRelatedField(source="department", slug_field="slug", read_only=True)

    class Meta:
        model = Scheme
        fields = [
            "id", "slug", "name_hi", "name_en", "overview_hi", "overview_en",
            "benefits_hi", "benefits_en", "eligibility_hi", "eligibility_en",
            "process_hi", "process_en", "image", "department_slug", "apply_url",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
