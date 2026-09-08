from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("text_en", "show_in_ticker", "show_in_sidebar", "order", "is_published")
    list_editable = ("show_in_ticker", "show_in_sidebar", "order", "is_published")
