from django.contrib import admin
from literals.models import University
# Register your models here.


admin.site.site_header = "ROOMBRL ADMINISTRATOR"
admin.site.site_title = "ROOMBRL PORTAL"
admin.site.index_title = "ROOMBRL  ADMINISTRATOR PORTAL"


@admin.register(University)
class LiteralsAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
