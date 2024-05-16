from account.models import User, UserAdditionalDetail
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(User)
class UserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(UserAdditionalDetail)
class UserAdditionalDetailAdmin(admin.ModelAdmin):
    list_display = ["user", "other_name", "guardian_full_name",
                    "ghana_card_number", 'institution']
