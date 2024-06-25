from comments.models import Comment
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

# Register your models here.


class CustomMPTTModelAdmin(MPTTModelAdmin):
    list_display = [
        "content",
        "created_by",
    ]
    mptt_level_indent = 30


admin.site.register(Comment, CustomMPTTModelAdmin)
