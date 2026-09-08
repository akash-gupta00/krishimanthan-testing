from django.contrib import admin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_hi", "slug", "order", "is_published")
    list_editable = ("order", "is_published")
    prepopulated_fields = {"slug": ("name_en",)}
    search_fields = ("name_en", "name_hi")
