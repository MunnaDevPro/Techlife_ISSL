from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Comment, Reply


class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 0
    verbose_name_plural = "Replies"
    classes = ["collapse"]  # collapsible inline section


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ("post_title", "user_name", "short_content", "created_at")
    list_filter = ("created_at",)
    search_fields = ("post__title", "user__first_name", "content")
    ordering = ("-created_at",)
    inlines = [ReplyInline]
    list_per_page = 20

    # Grouped fieldsets for better UI
    fieldsets = (
        ("Post & User Info", {
            "fields": ("post", "user"),
            "classes": ("wide",)
        }),
        ("Comment Content", {
            "fields": ("content",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    readonly_fields = ("created_at", "updated_at")

    # custom display methods
    def post_title(self, obj):
        return obj.post.title
    post_title.short_description = "Post"

    def user_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}' 
    user_name.short_description = "User"

    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
    short_content.short_description = "Comment"


@admin.register(Reply)
class ReplyAdmin(ModelAdmin):
    list_display = ("comment_preview", "user_name", "short_content", "created_at")
    list_filter = ("created_at",)
    search_fields = ("comment__content", "user__first_name", "content")
    ordering = ("-created_at",)
    list_per_page = 20

    fieldsets = (
        ("Comment & User Info", {
            "fields": ("comment", "user"),
        }),
        ("Reply Content", {
            "fields": ("content",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    readonly_fields = ("created_at", "updated_at")

    def comment_preview(self, obj):
        return obj.comment.content[:40] + ("..." if len(obj.comment.content) > 40 else "")
    comment_preview.short_description = "Comment"

    def user_name(self, obj):
        return obj.user.first_name
    user_name.short_description = "User"

    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
    short_content.short_description = "Reply"
