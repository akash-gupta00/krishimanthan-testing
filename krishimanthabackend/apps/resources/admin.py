from django.contrib import admin
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("name_en", "order", "is_published")
    list_editable = ("order", "is_published")
    search_fields = ("name_en", "name_hi")
