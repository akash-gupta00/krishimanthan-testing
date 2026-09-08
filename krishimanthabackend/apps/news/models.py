from django.db import models
from tinymce.models import HTMLField
from apps.core.models import TimeStampedModel, PublishableModel, SEOModel
from apps.departments.models import Department
from apps.core.validators import validate_image_file


class NewsCategory(TimeStampedModel):
    name_hi = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name_en"]
        verbose_name_plural = "News categories"

    def __str__(self):
        return self.name_en


class NewsItem(TimeStampedModel, PublishableModel, SEOModel):
    title_hi = models.CharField(max_length=300)
    title_en = models.CharField(max_length=300)
    summary_hi = models.TextField()
    summary_en = models.TextField()
    content_hi = HTMLField(blank=True, help_text="Full article body (Hindi).")
    content_en = HTMLField(blank=True, help_text="Full article body (English).")
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, related_name="news_items")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="news_items")
    image = models.ImageField(upload_to="news/%Y/%m/", validators=[validate_image_file])
    author = models.CharField(max_length=150, default="Krishi Manthan Desk")
    published_date = models.DateField()

    class Meta:
        ordering = ["-published_date", "-created_at"]

    def __str__(self):
        return self.title_en
