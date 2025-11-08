from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Tag


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ("name", "slug", "created_at", "tag_preview")
    search_fields = ("name", "slug")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    list_per_page = 20

    fieldsets = (
        ("Tag Information", {
            "fields": ("name", "slug"),
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )

    readonly_fields = ("created_at",)

    def tag_preview(self, obj):
        return f"#{obj.name.lower()}"
    tag_preview.short_description = "Preview"
