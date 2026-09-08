from django.db import models
from apps.core.models import TimeStampedModel, PublishableModel
from apps.core.validators import validate_image_file


class Testimonial(TimeStampedModel, PublishableModel):
    name = models.CharField(max_length=150)
    role_hi = models.CharField(max_length=150, blank=True)
    role_en = models.CharField(max_length=150, blank=True)
    quote_hi = models.TextField()
    quote_en = models.TextField()
    avatar = models.ImageField(upload_to="testimonials/", blank=True, null=True, validators=[validate_image_file])
    rating = models.PositiveSmallIntegerField(default=5)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.name
