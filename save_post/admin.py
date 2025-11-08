from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import SavedPost


@admin.register(SavedPost)
class SavedPostAdmin(ModelAdmin):
    list_display = ("user_name", "post_title", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__first_name", "user__email", "post__title")
    ordering = ("-created_at",)
    list_per_page = 25

    readonly_fields = ("created_at",)

    fieldsets = (
        ("Saved Post Info", {
            "fields": ("user", "post"),
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

    def user_name(self, obj):
        return obj.user.first_name or obj.user.email
    user_name.short_description = "Saved By"

    def post_title(self, obj):
        return obj.post.title
    post_title.short_description = "Post Title"
