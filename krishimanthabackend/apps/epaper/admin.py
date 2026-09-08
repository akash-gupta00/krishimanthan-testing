from django.contrib import admin
from .models import EPaperIssue


@admin.register(EPaperIssue)
class EPaperIssueAdmin(admin.ModelAdmin):
    list_display = ("title_en", "issue_date", "is_published")
    list_editable = ("is_published",)
    date_hierarchy = "issue_date"
