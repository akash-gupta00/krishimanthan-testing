from django.contrib import admin
from .models import AboutContent, AboutHighlight


@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not AboutContent.objects.exists()


@admin.register(AboutHighlight)
class AboutHighlightAdmin(admin.ModelAdmin):
    list_display = ("title_en", "icon", "order", "is_published")
    list_editable = ("order", "is_published")
