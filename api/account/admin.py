from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import User


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

