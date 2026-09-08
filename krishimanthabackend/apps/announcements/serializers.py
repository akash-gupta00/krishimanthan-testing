from rest_framework import serializers
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ["id", "text_hi", "text_en", "link_url", "show_in_ticker", "show_in_sidebar"]
