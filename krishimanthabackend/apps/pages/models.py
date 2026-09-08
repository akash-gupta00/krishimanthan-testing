from django.db import models
from tinymce.models import HTMLField


class StaticPage(models.Model):
    """Admin-editable long-form pages — Privacy Policy, Terms & Conditions,
    and any other one-off legal/info page. Content uses a rich text
    (TinyMCE) editor so admins can format it without touching code."""
    slug = models.SlugField(max_length=100, unique=True, help_text="URL path, e.g. 'privacy-policy' or 'terms-conditions'.")
    title_hi = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    content_hi = HTMLField()
    content_en = HTMLField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return self.title_en
