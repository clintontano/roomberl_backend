from django_filters import rest_framework as filters
from room.models import Room
from room.models import RoomPricing


class RoomFilter(filters.FilterSet):
    class Meta:
        model = Room
        fields = [
            "id",
            "hostel",
            "room_type",
            "code",
            "floor_plane",
        ]


class RoomPricingFilter(filters.FilterSet):
    class Meta:
        model = RoomPricing
        fields = [
            "id",
            "room",
            "semester",
            "year",
            "due_date",
            "length_of_stay",
        ]
