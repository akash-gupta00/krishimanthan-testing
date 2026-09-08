from rest_framework import serializers
from .models import EPaperIssue


class EPaperIssueSerializer(serializers.ModelSerializer):
    pdf_file = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = EPaperIssue
        fields = ["id", "title_hi", "title_en", "issue_date", "pdf_file", "thumbnail"]

    def get_pdf_file(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pdf_file.url) if request and obj.pdf_file else (obj.pdf_file.url if obj.pdf_file else None)

    def get_thumbnail(self, obj):
        request = self.context.get("request")
        if obj.thumbnail and hasattr(obj.thumbnail, "url"):
            return request.build_absolute_uri(obj.thumbnail.url) if request else obj.thumbnail.url
        return None
