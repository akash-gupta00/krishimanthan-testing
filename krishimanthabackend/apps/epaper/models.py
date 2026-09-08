from django.db import models
from apps.core.models import TimeStampedModel, PublishableModel
from apps.core.validators import validate_image_file, validate_pdf_file


class EPaperIssue(TimeStampedModel, PublishableModel):
    title_hi = models.CharField(max_length=200, default="कृषि मंथन ई-पेपर")
    title_en = models.CharField(max_length=200, default="Krishi Manthan E-paper")
    issue_date = models.DateField(unique=True)
    pdf_file = models.FileField(upload_to="epaper/pdf/%Y/%m/", validators=[validate_pdf_file])
    thumbnail = models.ImageField(upload_to="epaper/thumb/%Y/%m/", blank=True, null=True, validators=[validate_image_file])

    class Meta:
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.title_en} - {self.issue_date}"
