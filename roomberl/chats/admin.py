from chats.models import Chat
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

# Register your models here.


class CustomMPTTModelAdmin(MPTTModelAdmin):
    list_display = [
        "content",
    ]
    mptt_level_indent = 30


admin.site.register(Chat, CustomMPTTModelAdmin)
