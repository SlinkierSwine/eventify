from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import SocialAccount, User


@admin.register(User)
class AccountAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "is_staff",
        "created_at",
        "updated_at",
    )
    search_fields = ("email",)
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = ()
    filter_horizontal = ()
    ordering = ("-created_at",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                ),
            },
        ),
    )


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "user", "use_for_notifications")
