from chats.models import Chat
from chats.models import ChatRoom
from django.contrib import admin

# Register your models here.


class ChatInline(admin.TabularInline):
    model = Chat


@admin.register(ChatRoom)
class CustomMPTTModelAdmin(admin.ModelAdmin):
    inlines = [ChatInline]
    list_display = [
        "name",
    ]
    # mptt_level_indent = 30
