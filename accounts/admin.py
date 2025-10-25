from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUserModel



admin.site.site_header = "TechLife Administration"
admin.site.site_title = "TechLife Admin"
admin.site.index_title = "Welcome to TechLife Control Panel"



@admin.register(CustomUserModel)
class CustomUserAdmin(UserAdmin):
    model = CustomUserModel
    list_display = ( "email", "id", "is_verified", "first_name", "last_name", "mobile", "is_active", "is_staff")
    list_filter = ("is_verified", "is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name", "mobile")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "password", "is_verified")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "profile_picture", "mobile")}),
        ("Address", {"fields": ("address_line_1", "address_line_2", "city", "postcode", "country")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_verified", "is_active", "is_staff"),
        }),
    )