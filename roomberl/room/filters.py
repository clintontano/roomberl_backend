from django_filters import rest_framework as filters
from room.models import Room
from room.models import RoomType


class RoomFilter(filters.FilterSet):
    class Meta:
        model = Room
        fields = [
            "id",
            "hostel",
            "room_type",
            "code",
        ]


class RoomTypeFilter(filters.FilterSet):
    class Meta:
        model = RoomType
        fields = [
            "id",
            "hostel",
        ]
