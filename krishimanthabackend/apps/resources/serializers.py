from rest_framework import serializers
from .models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = ["id", "name_hi", "name_en", "desc_hi", "desc_en", "file", "icon"]

    def get_file(self, obj):
        request = self.context.get("request")
        if obj.file and hasattr(obj.file, "url"):
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None
