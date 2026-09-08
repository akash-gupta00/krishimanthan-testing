from django.contrib import admin
from .models import Advertisement, AdSlot


@admin.register(AdSlot)
class AdSlotAdmin(admin.ModelAdmin):
    list_display = ("name", "key")


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "slot", "advertiser_name", "duration_days", "status", "start_date", "end_date")
    list_filter = ("status", "slot", "duration_days")
    list_editable = ("status",)
    search_fields = ("title", "advertiser_name", "advertiser_email")
    actions = ["approve_ads", "reject_ads"]

    @admin.action(description="Approve selected ads (starts today, ends after their requested duration)")
    def approve_ads(self, request, queryset):
        from django.utils import timezone
        for ad in queryset:
            ad.status = Advertisement.Status.APPROVED
            if not ad.start_date:
                ad.start_date = timezone.localdate()
            ad.save()

    @admin.action(description="Reject selected ads")
    def reject_ads(self, request, queryset):
        queryset.update(status=Advertisement.Status.REJECTED)
