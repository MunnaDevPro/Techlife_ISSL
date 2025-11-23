from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from .models import Favorite, Share


@admin.register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ("user_display", "post_display", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__email", "user__first_name", "post__title")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    list_per_page = 25

    fieldsets = (
        ("Favorite Info", {
            "fields": ("user", "post"),
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

    def user_display(self, obj):
        return format_html(
            '<span style="padding:3px 6px;border-radius:6px;">{}</span>',
            f"{obj.user.first_name } {obj.user.last_name}" 
        )
    user_display.short_description = "User"

    def post_display(self, obj):
        return format_html(
            '<span style="color:#1565c0;font-weight:500;">{}</span>',
            obj.post.title
        )
    post_display.short_description = "Post"


@admin.register(Share)
class ShareAdmin(ModelAdmin):
    list_display = ("post_display", "user_display", "platform_badge", "created_at")
    list_filter = ("platform", "created_at")
    search_fields = ("post__title", "user__email", "platform")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    list_per_page = 5

    fieldsets = (
        ("Share Info", {
            "fields": ("post", "user", "platform"),
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

    def post_display(self, obj):
        return format_html(
            '<span style="color:#1e88e5;font-weight:500;">{}</span>',
            obj.post.title
        )
    post_display.short_description = "Post"

    def user_display(self, obj):
        if obj.user:
            return format_html(
                '<span style="padding:3px 6px;border-radius:6px;">{}</span>',
                f"{obj.user.first_name } {obj.user.last_name}"
            )
        return format_html('<span style="color:#9e9e9e;">Anonymous</span>')
    user_display.short_description = "User"

    def platform_badge(self, obj):
        colors = {
            "facebook": "#1877f2",
            "linkedin": "#0077b5",
            "twitter": "#1da1f2",
            "whatsapp": "#25d366",
        }
        color = colors.get(obj.platform, "#757575")
        return format_html(
            '<span style="background:{};color:white;padding:3px 8px;border-radius:6px;text-transform:capitalize;">{}</span>',
            color,
            obj.platform
        )
    platform_badge.short_description = "Platform"
