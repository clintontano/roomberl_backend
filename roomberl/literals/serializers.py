from literals.models import RoomType
from literals.models import University
from rest_framework import serializers


class ListAllLiteralsSerializer(serializers.Serializer):
    universities = serializers.SerializerMethodField()
    room_types = serializers.SerializerMethodField()

    def get_universities(self, obj: University):
        return University.objects.values()

    def get_room_types(self, obj: RoomType):
        return RoomType.objects.values()
