from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title_en", "event_date", "is_upcoming", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title_en", "title_hi")
    prepopulated_fields = {"slug": ("title_en",)}
    date_hierarchy = "event_date"

    @admin.display(boolean=True, description="Upcoming?")
    def is_upcoming(self, obj):
        return obj.is_upcoming
