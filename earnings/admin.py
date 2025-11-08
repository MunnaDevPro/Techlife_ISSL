from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from .models import EarningSetting


@admin.register(EarningSetting)
class EarningSettingAdmin(ModelAdmin):
    list_display = ("colored_view_rate", "colored_like_rate", "colored_comment_rate", "colored_quality_rate", "updated_at_display")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-updated_at",)
    list_per_page = 10

    fieldsets = (
        ("Earning Rates", {
            "fields": ("view_rate", "like_rate", "comment_rate", "quality_rate"),
            "description": "💰 Configure how much each user earns per engagement type.",
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def colored_view_rate(self, obj):
        return format_html('<span style="color:#43a047;font-weight:600;">{} ৳ / view</span>', obj.view_rate)
    colored_view_rate.short_description = "View Rate"

    def colored_like_rate(self, obj):
        return format_html('<span style="color:#1e88e5;font-weight:600;">{} ৳ / like</span>', obj.like_rate)
    colored_like_rate.short_description = "Like Rate"

    def colored_comment_rate(self, obj):
        return format_html('<span style="color:#f4511e;font-weight:600;">{} ৳ / comment</span>', obj.comment_rate)
    colored_comment_rate.short_description = "Comment Rate"

    def colored_quality_rate(self, obj):
        return format_html('<span style="color:#8e24aa;font-weight:600;">{} ৳ / quality</span>', obj.quality_rate)
    colored_quality_rate.short_description = "Quality Rate"

    def updated_at_display(self, obj):
        return format_html('<span style="color:#757575;">{}</span>', obj.updated_at.strftime("%b %d, %Y %I:%M %p"))
    updated_at_display.short_description = "Last Updated"
