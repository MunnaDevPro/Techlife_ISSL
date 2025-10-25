from django.contrib import admin
from .models import contact_or_support


@admin.register(contact_or_support)
class ContactOrSupportAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "user", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    fieldsets = (
        ("User Info", {
            "fields": ("user", "name", "email", "phone")
        }),
        ("Message Details", {
            "fields": ("message",)
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )
