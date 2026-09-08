from django.db import models
from apps.core.models import TimeStampedModel, PublishableModel


class MarketPrice(TimeStampedModel, PublishableModel):
    class Trend(models.TextChoices):
        UP = "up", "Up"
        DOWN = "down", "Down"
        FLAT = "flat", "Flat"

    crop_name_hi = models.CharField(max_length=100)
    crop_name_en = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_hi = models.CharField(max_length=50, default="क्विंटल")
    unit_en = models.CharField(max_length=50, default="qtl")
    trend = models.CharField(max_length=10, choices=Trend.choices, default=Trend.FLAT)

    class Meta:
        ordering = ["order", "crop_name_en"]

    def __str__(self):
        return f"{self.crop_name_en} - {self.price}"
