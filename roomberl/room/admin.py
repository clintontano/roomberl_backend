from django.contrib import admin
from room.models import Room
from room.models import RoomImage

# Register your models here.


class RoomImageInline(admin.TabularInline):
    model = RoomImage


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "room_type", "name", "code", "description", "floor_plane"]
    list_filter = [
        "room_type",
    ]
    search_fields = ["room_type", "code", "description", "floor_plane"]
    list_display_links = ["room_type"]
