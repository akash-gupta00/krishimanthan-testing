from rest_framework import serializers
from .models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    favicon = serializers.SerializerMethodField()
    og_image = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = [
            "site_name", "tagline_hi", "tagline_en", "logo", "favicon",
            "address_hi", "address_en", "email", "phone",
            "facebook_url", "twitter_url", "youtube_url", "whatsapp_url",
            "default_meta_title", "default_meta_description", "default_meta_keywords", "og_image",
        ]

    def _abs(self, obj_field):
        request = self.context.get("request")
        if obj_field and hasattr(obj_field, "url"):
            return request.build_absolute_uri(obj_field.url) if request else obj_field.url
        return None

    def get_logo(self, obj):
        return self._abs(obj.logo)

    def get_favicon(self, obj):
        return self._abs(obj.favicon)

    def get_og_image(self, obj):
        return self._abs(obj.og_image)
