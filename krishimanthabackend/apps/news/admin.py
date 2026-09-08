from django.contrib import admin
from .models import NewsItem, NewsCategory


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_hi", "slug", "order")
    prepopulated_fields = {"slug": ("name_en",)}


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title_en", "category", "department", "published_date", "is_published")
    list_filter = ("category", "department", "is_published")
    list_editable = ("is_published",)
    search_fields = ("title_en", "title_hi", "summary_en", "summary_hi")
    prepopulated_fields = {"slug": ("title_en",)}
    date_hierarchy = "published_date"
    fieldsets = (
        (None, {"fields": ("title_hi", "title_en", "slug", "category", "department", "image", "author", "published_date", "is_published", "order")}),
        ("Content", {"fields": ("summary_hi", "summary_en", "content_hi", "content_en")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "meta_keywords"), "classes": ("collapse",)}),
    )
