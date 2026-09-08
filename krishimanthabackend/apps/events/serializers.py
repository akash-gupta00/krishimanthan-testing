from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    is_upcoming = serializers.BooleanField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "slug", "title_hi", "title_en", "desc_hi", "desc_en",
            "event_date", "location_hi", "location_en", "organizer_hi", "organizer_en",
            "image", "registration_url", "is_upcoming",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
