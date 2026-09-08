from rest_framework import serializers
from .models import StaticPage


class StaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPage
        fields = ["slug", "title_hi", "title_en", "content_hi", "content_en", "updated_at"]
