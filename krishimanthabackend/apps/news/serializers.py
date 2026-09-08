from rest_framework import serializers
from .models import NewsItem, NewsCategory


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ["id", "name_hi", "name_en", "slug"]


class NewsItemListSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = NewsItem
        fields = [
            "id", "slug", "title_hi", "title_en", "summary_hi", "summary_en",
            "category", "image", "author", "published_date",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class NewsItemDetailSerializer(NewsItemListSerializer):
    class Meta(NewsItemListSerializer.Meta):
        fields = NewsItemListSerializer.Meta.fields + [
            "content_hi", "content_en", "meta_title", "meta_description", "meta_keywords",
        ]
