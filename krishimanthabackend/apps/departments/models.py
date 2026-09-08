from django.db import models
from apps.core.models import TimeStampedModel, PublishableModel


class Department(TimeStampedModel, PublishableModel):
    name_hi = models.CharField(max_length=120)
    name_en = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description_hi = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="Wheat", help_text="Lucide icon name used by the frontend, e.g. Wheat, Building2, TreePine, PawPrint.")
    color_tone = models.CharField(max_length=50, default="bg-green-100 text-green-700", help_text="Tailwind classes for the icon badge tone.")

    class Meta:
        ordering = ["order", "name_en"]

    def __str__(self):
        return self.name_en
