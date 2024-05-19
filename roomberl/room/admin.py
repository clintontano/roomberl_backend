from django.contrib import admin
from room.models import Room
from room.models import RoomImage
from room.models import RoomPricing

# Register your models here.


class RoomImageInline(admin.TabularInline):
    model = RoomImage


class RoomPricingInline(admin.TabularInline):
    model = RoomPricing


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "room_type", "name", "code", "description", "floor_plane"]
    list_filter = [
        "room_type",
    ]
    search_fields = ["room_type", "code", "description", "floor_plane"]
    list_display_links = ["room_type"]

    inlines = [RoomImageInline, RoomPricingInline]
