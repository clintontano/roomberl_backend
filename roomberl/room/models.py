from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models
from literals.models import Hostel
from literals.models import RoomType
from literals.models import Semester
from literals.models import Year


class Room(BaseModel):
    roomimage_set: "RoomImage"
    roompricing_set: "RoomPricing"
    hostel = models.ForeignKey(Hostel, on_delete=models.PROTECT)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200, null=True, blank=True)
    floor_plane = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to="room/%Y-%m-%d", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} {self.room_type.name}"


class RoomImage(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="room/%Y-%m-%d")


class RoomPricing(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    year = models.ForeignKey(Year, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateTimeField(null=True, blank=True)
    length_of_stay = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True
    )

    def __str__(self) -> str:
        return f"{self.room.name} {self.room.room_type.name}"
