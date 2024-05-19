from literals.models import Hostel
from literals.models import RoomType
from literals.models import Semester
from literals.models import University
from literals.models import Year
from rest_framework import serializers


class ListAllLiteralsSerializer(serializers.Serializer):
    universities = serializers.SerializerMethodField()
    room_types = serializers.SerializerMethodField()

    hostels = serializers.SerializerMethodField()
    semesters = serializers.SerializerMethodField()
    years = serializers.SerializerMethodField()

    def get_universities(self, obj: University):
        return University.objects.values()

    def get_room_types(self, obj: RoomType):
        return RoomType.objects.values()

    def get_hostels(self, obj):
        return Hostel.objects.values()

    def get_semesters(self, obj):
        return Semester.objects.values()

    def get_years(self, obj):
        return Year.objects.values()
