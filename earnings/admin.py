from django.contrib import admin
from .models import EarningSetting


@admin.register(EarningSetting)
class EarningSettingAdmin(admin.ModelAdmin):
    list_display = (
        "updated_at",
        "view_rate",
        "like_rate",
        "comment_rate",

    )
    list_editable = (
        "view_rate",
        "like_rate",
        "comment_rate",

    )
    readonly_fields = ("updated_at",)
    ordering = ("-updated_at",)
    list_filter = ("updated_at",)



# @admin.register(ContentQuality)
# class ContentQualityAdmin(admin.ModelAdmin):
#     list_display = ("post", "content_score", "evaluated_at")
#     search_fields = ("post__title",)
#     autocomplete_fields = ("post",)
#     readonly_fields = ("evaluated_at",)
#     ordering = ("-evaluated_at",)
#     list_filter = ("evaluated_at",)
