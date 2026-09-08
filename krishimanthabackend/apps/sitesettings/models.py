from django.db import models
from apps.core.validators import validate_image_file


class SiteSettings(models.Model):
    """Singleton — global site identity, contact info & social links used
    across Header/Footer/Contact page/SEO defaults."""
    site_name = models.CharField(max_length=150, default="Krishi Manthan")
    tagline_hi = models.CharField(max_length=250, blank=True)
    tagline_en = models.CharField(max_length=250, blank=True)
    logo = models.ImageField(upload_to="site/", blank=True, null=True, validators=[validate_image_file])
    favicon = models.ImageField(upload_to="site/", blank=True, null=True, validators=[validate_image_file])

    address_hi = models.CharField(max_length=300, blank=True)
    address_en = models.CharField(max_length=300, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    whatsapp_url = models.URLField(blank=True)

    default_meta_title = models.CharField(max_length=200, blank=True)
    default_meta_description = models.CharField(max_length=300, blank=True)
    default_meta_keywords = models.CharField(max_length=300, blank=True)
    og_image = models.ImageField(upload_to="site/", blank=True, null=True, validators=[validate_image_file])

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"site_name": "Krishi Manthan"})
        return obj
