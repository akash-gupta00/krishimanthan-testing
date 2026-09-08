from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from apps.core.validators import validate_image_file, validate_pdf_file


class AdSlot(models.Model):
    """The fixed set of ad positions that exist in the frontend UI —
    matches Sidebar (top/bottom), Footer banner, News inline, Home banner."""
    key = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.name


class Advertisement(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    class Duration(models.IntegerChoices):
        SEVEN_DAYS = 7, "7 days"
        FIFTEEN_DAYS = 15, "15 days"
        THIRTY_DAYS = 30, "30 days"

    slot = models.ForeignKey(AdSlot, on_delete=models.CASCADE, related_name="ads")
    title = models.CharField(max_length=200)
    advertiser_name = models.CharField(max_length=200)
    advertiser_email = models.EmailField()
    advertiser_phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="ads/%Y/%m/", blank=True, null=True, validators=[validate_image_file])
    pdf_file = models.FileField(upload_to="ads/pdf/%Y/%m/", blank=True, null=True, validators=[validate_pdf_file])
    link_url = models.URLField(blank=True)
    duration_days = models.PositiveSmallIntegerField(choices=Duration.choices, default=Duration.SEVEN_DAYS, help_text="Requested run length, in days — chosen by the advertiser when submitting.")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.slot.key})"

    def save(self, *args, **kwargs):
        # Auto-compute end_date from the requested duration the first time
        # an admin approves the ad (start_date set), so the run length the
        # advertiser asked for is honoured without manual date maths.
        if self.status == self.Status.APPROVED and self.start_date and not self.end_date:
            from datetime import timedelta
            self.end_date = self.start_date + timedelta(days=self.duration_days)
        super().save(*args, **kwargs)

    @property
    def is_currently_active(self):
        if self.status != self.Status.APPROVED:
            return False
        today = timezone.localdate()
        if self.start_date and today < self.start_date:
            return False
        if self.end_date and today > self.end_date:
            return False
        return True
