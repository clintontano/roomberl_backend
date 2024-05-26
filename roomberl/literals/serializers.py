from literals.models import Hostel
from rest_framework import serializers


class ListAllLiteralsSerializer(serializers.Serializer):
    hostels = serializers.SerializerMethodField()

    def get_hostels(self, obj):
        return Hostel.objects.values()


class UnauthenticatedLiteralsSerializer(serializers.Serializer):
    hostels = serializers.SerializerMethodField()

    def get_hostels(self, obj: Hostel):
        return Hostel.objects.values()
