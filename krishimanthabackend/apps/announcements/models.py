from django.db import models
from apps.core.models import TimeStampedModel, PublishableModel


class Announcement(TimeStampedModel, PublishableModel):
    """Feeds both the top-bar scrolling ticker AND the sidebar
    "Govt. Announcement" widget — `show_in_ticker` / `show_in_sidebar`
    let admin decide where each one appears."""
    text_hi = models.CharField(max_length=300)
    text_en = models.CharField(max_length=300)
    link_url = models.URLField(blank=True)
    show_in_ticker = models.BooleanField(default=True)
    show_in_sidebar = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.text_en[:60]
