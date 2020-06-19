from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.contrib.auth import get_user_model


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "last_login",
                    "rut",
                    "first_name",
                    "last_name",
                    "cargo",
                    "celular",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("rut", "email", "password1",)}),
    )

    list_display = ("email", "is_staff", "last_login")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(User)
