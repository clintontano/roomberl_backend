from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from room.models import Room
from room.serializers import RoomSerializer


class RoomApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
