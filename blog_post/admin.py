from django.contrib import admin
from blog_post.models import Post_view_ip, Category, BlogPost,Review ,BlogAdditionalImage, Like



class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class BlogAdditionalImageInline(admin.TabularInline):
    model = BlogAdditionalImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    search_fields = ("name",)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "created_at")
    list_filter = ("status", "category")
    search_fields = ("title", "author__email", "category__name")
    inlines = [ReviewInline, BlogAdditionalImageInline]

@admin.register(BlogAdditionalImage)
class BlogAdditionalImageAdmin(admin.ModelAdmin):
    list_display = ("blog", "preview_image", "additional_image_url")
    search_fields = ("blog__title",)
    autocomplete_fields = ("blog",)

    def preview_image(self, obj):
        if obj.additional_image:
            return f" {obj.additional_image.url}"
        return "No Image"
    preview_image.short_description = "Image"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "star_rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("post__title", "user__email")
    autocomplete_fields = ("post", "user")

    def star_rating(self, obj):
        return "⭐" * obj.rating 
    star_rating.short_description = "Rating"

admin.site.register(Post_view_ip)




@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):

    list_display = ("post_title", "user_email", "created_at")

    list_filter = ("created_at",)
    
    search_fields = ("post__title", "user__email")
    

    autocomplete_fields = ("post", "user")

  
    def post_title(self, obj):
        return obj.post.title
    post_title.short_description = "Blog Post"


    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "User (Email)"