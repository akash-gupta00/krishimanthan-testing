from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from apps.core.models import TimeStampedModel, PublishableModel, SEOModel
from apps.departments.models import Department
from apps.core.validators import validate_image_file


class Event(TimeStampedModel, PublishableModel, SEOModel):
    title_hi = models.CharField(max_length=250)
    title_en = models.CharField(max_length=250)
    desc_hi = HTMLField(blank=True)
    desc_en = HTMLField(blank=True)
    event_date = models.DateField()
    location_hi = models.CharField(max_length=250)
    location_en = models.CharField(max_length=250)
    organizer_hi = models.CharField(max_length=250)
    organizer_en = models.CharField(max_length=250)
    image = models.ImageField(upload_to="events/%Y/%m/", validators=[validate_image_file])
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")
    registration_url = models.URLField(blank=True)

    class Meta:
        ordering = ["event_date"]

    def __str__(self):
        return self.title_en

    @property
    def is_upcoming(self):
        """Computed automatically from today's date — no manual flag to maintain."""
        return self.event_date >= timezone.localdate()
