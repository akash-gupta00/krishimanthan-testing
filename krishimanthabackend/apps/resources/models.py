from django.db import models
from apps.core.models import TimeStampedModel, PublishableModel
from apps.core.validators import validate_pdf_file


class Resource(TimeStampedModel, PublishableModel):
    name_hi = models.CharField(max_length=250)
    name_en = models.CharField(max_length=250)
    desc_hi = models.TextField(blank=True)
    desc_en = models.TextField(blank=True)
    file = models.FileField(upload_to="resources/%Y/%m/", help_text="PDF to download.", validators=[validate_pdf_file])
    icon = models.CharField(max_length=50, default="FileDown")

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.name_en
