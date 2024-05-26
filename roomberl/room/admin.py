from django.contrib import admin
from room.models import Room
from room.models import RoomAmenity
from room.models import RoomImage
from room.models import RoomType

# Register your models here.


class RoomImageInline(admin.TabularInline):
    model = RoomImage


class RoomInline(admin.TabularInline):
    model = Room


class RoomTypeInline(admin.TabularInline):
    model = RoomType


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price"]


@admin.register(RoomAmenity)
class RoomAmenitiesAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(Room)
class RoomAdminAdmin(admin.ModelAdmin):
    list_display = ["name", "room_type", "name", "code", "description"]
    list_filter = [
        "room_type",
    ]
    search_fields = ["room_type", "code", "description"]
    list_display_links = ["room_type"]

    inlines = [RoomImageInline]
