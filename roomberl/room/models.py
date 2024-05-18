from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models
from literals.models import RoomType

# Create your models here.


class Room(BaseModel):
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200, null=True, blank=True)
    floor_plane = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class RoomImage(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="room/%Y-%m-%d")
