from django.db import models
from tinymce.models import HTMLField
from apps.core.models import TimeStampedModel, PublishableModel, SEOModel
from apps.departments.models import Department
from apps.core.validators import validate_image_file


class Scheme(TimeStampedModel, PublishableModel, SEOModel):
    name_hi = models.CharField(max_length=250)
    name_en = models.CharField(max_length=250)
    overview_hi = models.TextField()
    overview_en = models.TextField()
    benefits_hi = HTMLField()
    benefits_en = HTMLField()
    eligibility_hi = HTMLField()
    eligibility_en = HTMLField()
    process_hi = HTMLField()
    process_en = HTMLField()
    image = models.ImageField(upload_to="schemes/%Y/%m/", validators=[validate_image_file])
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="schemes")
    apply_url = models.URLField(blank=True, help_text="Official application link, if available.")

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.name_en
