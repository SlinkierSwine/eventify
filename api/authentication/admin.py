from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.models import User


@admin.register(User)
class AccountAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "is_staff",
        "created_at",
        "updated_at",
    )
    search_fields = ("username",)
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = ()
    ordering = ("-created_at",)

