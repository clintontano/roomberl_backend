from django.contrib import admin
from literals.models import Hostel
from literals.models import HostelPaymentDetail
from literals.models import Institution


# Register your models here.


admin.site.site_header = "ROOMBERL ADMINISTRATOR"
admin.site.site_title = "ROOMBERL PORTAL"
admin.site.index_title = "ROOMBERL  ADMINISTRATOR PORTAL"


class HostelPaymentDetailsAdmin(admin.TabularInline):
    model = HostelPaymentDetail
    extra = 2


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    inlines = [HostelPaymentDetailsAdmin]
    list_display = [
        "name",
        "description",
        "code",
        "owner_name",
        "owner_email",
        "owner_phone",
    ]
    readonly_fields = ["code"]


admin.site.register([Institution])
