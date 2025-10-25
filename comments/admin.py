from django.contrib import admin
from .models import Comment, Reply


class commentReplyInline(admin.TabularInline):
    model = Reply
    extra = 0



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post__title", "user__first_name", "content", "created_at")
    list_filter = ("created_at",)
    search_fields = ("post__title", "user__first_name", "content")
    inlines = [commentReplyInline]




@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("comment__content", "user__first_name", "content", "created_at")
    list_filter = ("created_at",)
    search_fields = ("comment__content", "user__first_name", "content")
