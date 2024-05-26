from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models
from literals.models import Hostel


class RoomAmenity(BaseModel):
    roomtype_set: "RoomType"
    room_set: "Room"
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo = models.ImageField(blank=True, null=True, upload_to="room_amenities")


class RoomType(BaseModel):
    room_set: "Room"
    hostel = models.ForeignKey(Hostel, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    room_amenities = models.ManyToManyField(RoomAmenity, blank=True)


class Room(BaseModel):
    roomimage_set: "RoomImage"
    hostel = models.ForeignKey(Hostel, on_delete=models.PROTECT)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200, null=True, blank=True)
    floor_plan = models.ImageField(upload_to="floor_plan", null=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to="room/%Y-%m-%d", null=True, blank=True)
    room_amenities = models.ManyToManyField(RoomAmenity, blank=True)

    def __str__(self) -> str:
        return f"{self.name} {self.room_type.name}"


class RoomImage(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="room/%Y-%m-%d")
