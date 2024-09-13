from account.models import User
from account.serializers import SimpleUserAccountSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import serializers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
        if self.action == "list" and not hostel:
            raise serializers.ValidationError({"hostel": "This parameter is required."})
        if hostel:
            queryset = queryset.filter(hostel=hostel)
        return queryset


class RoomApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.order_by("updated_at")
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        hostel = self.request.query_params.get("hostel")
        if self.action == "list" and not hostel:
            raise serializers.ValidationError({"hostel": "This parameter is required."})
        if hostel:
            queryset = queryset.filter(hostel=hostel)
        return queryset


class DuplicateRoomApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        room_id = kwargs.get("pk")
        quantity = kwargs.get("quantity")

        if quantity > 20:
            raise serializers.ValidationError(
                code="Invalid_quantity", detail="maximum quantity allowed is 20"
            )

        original_room = get_object_or_404(Room, id=room_id)
        room_data = original_room.__dict__.copy()

        code = room_data.pop("code", None)

        room_data.pop("_state", None)
        room_data.pop("id", None)

        duplicated_rooms = []
        for count in range(quantity):
            new_room = Room.objects.create(
                **room_data,
                code=f"{code}-{count + 1}",
                created_by=self.request.user,
            )
            duplicated_rooms.append(new_room)

        serializer = self.get_serializer(duplicated_rooms, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ViewRoomMembersApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SimpleUserAccountSerializer

    def get_queryset(self):
        room_id = get_object_or_404(Room, id=self.kwargs.get("room_id"))
        return User.objects.filter(useradditionaldetail__room_id=room_id)
