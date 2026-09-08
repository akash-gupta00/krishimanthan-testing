from django.db import models
from tinymce.models import HTMLField
from apps.core.models import TimeStampedModel, PublishableModel


class AboutContent(models.Model):
    """Singleton — admin edits the one row that feeds the /about page intro."""
    intro_hi = HTMLField()
    intro_en = HTMLField()

    class Meta:
        verbose_name = "About page content"
        verbose_name_plural = "About page content"

    def __str__(self):
        return "About page content"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            "intro_hi": "", "intro_en": "",
        })
        return obj


class AboutHighlight(TimeStampedModel, PublishableModel):
    """The 3 "Our Mission / Our Audience / Our Purpose" cards on the About page."""
    title_hi = models.CharField(max_length=150)
    title_en = models.CharField(max_length=150)
    desc_hi = models.TextField()
    desc_en = models.TextField()
    icon = models.CharField(max_length=50, default="Target", help_text="Lucide icon name: Target, Users, BookOpen, etc.")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title_en
