from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from room.filters import RoomFilter
from room.filters import RoomTypeFilter
from room.models import Room
from room.models import RoomAmenity
from room.models import RoomType
from room.serializers import RoomAmenitySerializer
from room.serializers import RoomSerializer
from room.serializers import RoomTypeSerializer


class RoomAmenityApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = RoomAmenity.objects.order_by("updated_at")
    serializer_class = RoomAmenitySerializer


class RoomTypeApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = RoomType.objects.order_by("updated_at")
    serializer_class = RoomTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomTypeFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        hostel = self.request.query_params.get("hostel")
        if not hostel:
            raise serializers.ValidationError({"hostel": "This parameter is required."})
        return queryset.filter(hostel=hostel)


class RoomApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.order_by("updated_at")
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        hostel = self.request.query_params.get("hostel")
        if not hostel:
            raise serializers.ValidationError({"hostel": "This parameter is required."})
        return queryset.filter(hostel=hostel)
