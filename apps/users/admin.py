from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            None,
            {
                "fields": (
                    "email",
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
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "rut", "email", "cargo")
        }),
    )

    list_display = ("id", "username", "rut", "email", 'first_name', 'last_name', "is_staff", "cargo",
                    "format_last_login")
    list_filter = ("is_staff", "is_superuser", "is_active", "cargo", "groups")
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def format_last_login(self, obj):
        return obj.last_login.strftime("%d/%m/%Y %H:%M:%S") if obj.last_login else '-'

    format_last_login.short_description = 'last_login'
    format_last_login.admin_order_field = 'last_login'


admin.site.register(User, UserAdmin)
