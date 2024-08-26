from literals.models import Hostel
from literals.models import HostelPaymentDetail
from rest_framework import serializers
from room.models import RoomAmenity
from room.models import RoomType


class ListAllLiteralsSerializer(serializers.Serializer):
    hostels = serializers.SerializerMethodField()
    room_types = serializers.SerializerMethodField()
    room_amenities = serializers.SerializerMethodField()

    def get_hostels(self, obj):
        return Hostel.objects.values()

    def get_room_types(self, obj):
        return RoomType.objects.values()

    def get_room_amenities(self, obj):
        return RoomAmenity.objects.values()


class UnauthenticatedLiteralsSerializer(serializers.Serializer):
    hostels = serializers.SerializerMethodField()

    def get_hostels(self, obj: Hostel):
        return Hostel.objects.values()


class HostelPaymentDetailsSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="name")
    value = serializers.CharField(source="description")

    class Meta:
        model = HostelPaymentDetail
        fields = ["label", "value"]


class HostelSerializer(serializers.ModelSerializer):
    payment_details = HostelPaymentDetailsSerializer(
        read_only=True, many=True, source="hostelpaymentdetails_set"
    )

    class Meta:
        model = Hostel
        fields = "__all__"
