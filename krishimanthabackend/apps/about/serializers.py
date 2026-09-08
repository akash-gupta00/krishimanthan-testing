from rest_framework import serializers
from .models import AboutContent, AboutHighlight


class AboutHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutHighlight
        fields = ["id", "title_hi", "title_en", "desc_hi", "desc_en", "icon"]


class AboutContentSerializer(serializers.ModelSerializer):
    highlights = serializers.SerializerMethodField()

    class Meta:
        model = AboutContent
        fields = ["intro_hi", "intro_en", "highlights"]

    def get_highlights(self, obj):
        qs = AboutHighlight.objects.filter(is_published=True)
        return AboutHighlightSerializer(qs, many=True).data
