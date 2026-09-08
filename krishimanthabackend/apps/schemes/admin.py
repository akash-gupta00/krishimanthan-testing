from django.contrib import admin
from .models import Scheme


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ("name_en", "department", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("department", "is_published")
    search_fields = ("name_en", "name_hi")
    prepopulated_fields = {"slug": ("name_en",)}
    fieldsets = (
        (None, {"fields": ("name_hi", "name_en", "slug", "department", "image", "apply_url", "is_published", "order")}),
        ("Details", {"fields": ("overview_hi", "overview_en", "benefits_hi", "benefits_en", "eligibility_hi", "eligibility_en", "process_hi", "process_en")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "meta_keywords"), "classes": ("collapse",)}),
    )
