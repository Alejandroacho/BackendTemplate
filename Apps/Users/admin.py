from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django_rest_passwordreset.models import ResetPasswordToken
from Users.models import Profile
from Users.models import User


# Sets the admin logo
logo_url: str = "http://localhost:8000/static/logo.png"
admin.site.site_header = format_html(
    "<img src={url} height=50 width=50>", url=logo_url
)


# Sets the admin 'view site' url
site_url: str = settings.FRONTEND_URL
admin.site.site_url = site_url


# Sets the global admin titles
admin.site.site_title = settings.APP_NAME
admin.site.index_title = "Home"


# remove these lines if you want these models on admin
admin.site.unregister(Group)
admin.site.unregister(ResetPasswordToken)


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display: tuple = (
        "id",
        "email",
        "first_name",
        "is_verified",
        "is_premium",
    )
    list_display_links: tuple = ("id", "email")
    list_filter: tuple = ("is_admin", "is_verified", "is_premium")
    fieldsets: tuple = (
        ("General", {"fields": ("id", "email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "phone_number")},
        ),
        ("Account status", {"fields": ("is_verified", "is_premium")}),
        ("Permissions", {"fields": ("is_admin",)}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields: list = ["created_at", "updated_at", "id"]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets: tuple = (
        (
            "General",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields: tuple = ("email", "id")
    ordering: tuple = ("id", "email", "first_name")
    filter_horizontal: tuple = ()


class ProfileAdmin(admin.ModelAdmin):
    list_display: tuple = ("nickname", "gender", "birth_date")
    list_display_links: tuple = ("nickname",)
    list_filter: tuple = ("gender", "birth_date")
    fieldsets: tuple = (
        ("User", {"fields": ("user",)}),
        (
            "Personal info",
            {"fields": ("image", "birth_date", "gender")},
        ),
        ("Account info", {"fields": ("nickname", "bio")}),
    )
    search_fields: tuple = ("nickname", "id")
    ordering: tuple = ("user", "nickname", "gender", "birth_date")


class LogEntryAdmin(admin.ModelAdmin):
    list_display: tuple = (
        "user",
        "action_flag",
        "change_message",
    )
    search_fields: tuple = ("user__email",)
    date_hierarchy: str = "action_time"
    list_filter: tuple = ("action_flag", "content_type__model")
    list_per_page: int = 20


admin.site.register(User, UserAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Profile, ProfileAdmin)
