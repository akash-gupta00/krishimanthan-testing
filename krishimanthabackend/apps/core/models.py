from django.db import models


class TimeStampedModel(models.Model):
    """Adds created_at / updated_at to any model that inherits it."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishableModel(models.Model):
    """Content visibility toggle — lets admin hide content without deleting it."""
    is_published = models.BooleanField(default=True, help_text="Uncheck to hide from the public API without deleting.")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        abstract = True


class SEOModel(models.Model):
    """Per-record SEO fields — mirrors the frontend <SEO> component's props
    (title/description/keywords) so every dynamic page can get unique meta
    tags straight from the admin panel."""
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(max_length=220, unique=True)

    class Meta:
        abstract = True


class BilingualTextModel(models.Model):
    """Every public-facing model needs a Hindi + English pair for each
    field — matches the frontend's `t(hi, en)` translation pattern exactly,
    so API responses can be dropped straight into existing components."""

    class Meta:
        abstract = True
