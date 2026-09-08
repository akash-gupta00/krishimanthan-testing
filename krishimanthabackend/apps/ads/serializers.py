from rest_framework import serializers
from .models import Advertisement, AdSlot


class ActiveAdSerializer(serializers.ModelSerializer):
    """What the public site fetches to render a live ad slot."""
    image = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ["id", "title", "image", "link_url", "slot"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class AdSubmissionSerializer(serializers.ModelSerializer):
    """What the "Post Your Ads" form on the frontend submits — always lands
    in `pending` status for admin review, regardless of what's posted.
    `slot` is addressed by its human-readable key (e.g. "sidebar_top") so
    the frontend never needs to know internal numeric IDs."""

    slot = serializers.SlugRelatedField(slug_field="key", queryset=AdSlot.objects.all())

    class Meta:
        model = Advertisement
        fields = [
            "id", "slot", "title", "advertiser_name", "advertiser_email",
            "advertiser_phone", "description", "image", "pdf_file", "link_url", "duration_days",
        ]

    def create(self, validated_data):
        validated_data["status"] = Advertisement.Status.PENDING
        return super().create(validated_data)


class AdSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdSlot
        fields = ["key", "name", "description"]
