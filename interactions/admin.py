from django.contrib import admin
from .models import Favorite, Share

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")
    search_fields = ("post__title", "user__email")


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "platform", "created_at")
    list_filter = ("platform",)
