from account.models import RoomPayment
from account.models import User
from account.models import UserAdditionalDetail
from core.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class UserAdditionalDetailInine(admin.TabularInline):
    model = UserAdditionalDetail


class RoomPaymentInline(admin.TabularInline):
    model = RoomPayment


@admin.register(User)
class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    list_display = ["email", "first_name", "last_name", "hostel"]
    list_editable = ["hostel"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "hostel",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    inlines = [UserAdditionalDetailInine, RoomPaymentInline]


@admin.register(UserAdditionalDetail)
class UserAdditionalDetailAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "other_name",
        "guardian_full_name",
        "ghana_card_number",
    ]
