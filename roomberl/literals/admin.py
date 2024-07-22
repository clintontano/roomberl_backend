from django.contrib import admin
from literals.models import Hostel


# Register your models here.


admin.site.site_header = "ROOMBERL ADMINISTRATOR"
admin.site.site_title = "ROOMBERL PORTAL"
admin.site.index_title = "ROOMBERL  ADMINISTRATOR PORTAL"

admin.site.register([Hostel])
