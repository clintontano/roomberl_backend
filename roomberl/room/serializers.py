from core.serializers import BaseRoomBerlSerializer
from core.serializers import BaseToRepresentation
from core.serializers import CreatedByMixin
from django.conf import settings
from rest_framework import serializers
from room.models import Room
from room.models import RoomAmenity
from room.models import RoomImage
from room.models import RoomType


class RoomAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAmenity
        exclude = ["is_deleted"]


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        exclude = ["is_deleted"]

        extra_kwargs = {
            "pk": {"read_only": True},
            "hostel": {"required": True},
        }

    def get_is_fully_occupied(self, obj: RoomType):
        from account.models import RoomPayment

        available_rooms = obj.room_set.filter(is_locked=False).count()
        max_occupancy = available_rooms * obj.num_occupancy
        current_occupancy = RoomPayment.objects.filter(
            room_type=obj, is_verified=True
        ).count()

        return current_occupancy >= max_occupancy

    def validate(self, data):
        name = data.get("name")
        hostel = data.get("hostel")

        name_exist = RoomType.objects.filter(name=name, hostel=hostel).exists()

        if self.context["request"].method == "POST" and name_exist:
            raise serializers.ValidationError(
                f"this room  type already exists in {hostel.name}"
            )

        return data

    def to_representation(self, instance: RoomType):
        serializer = BaseRoomBerlSerializer(instance=instance)
        serializer.Meta.model = instance.__class__
        serializer.Meta.depth = 1

        data = serializer.to_representation(instance)

        data["is_fully_occupied"] = self.get_is_fully_occupied(instance)
        data["current_occupancy"] = instance.current_occupancy

        return data


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ["id", "room", "image"]


class RoomSerializer(CreatedByMixin, BaseToRepresentation, serializers.ModelSerializer):
    id = serializers.ReadOnlyField()  # noqa
    images = serializers.ListField(
        write_only=True,
        help_text="upload single or multiple files",
        required=False,
        child=serializers.FileField(
            max_length=settings.FILEFIELD_MAX_LENGTH,
            allow_empty_file=False,
            required=False,
            use_url=False,
        ),
    )

    class Meta:
        model = Room
        exclude = ["is_deleted"]
        read_only_fields = ["id", "created_by"]

        extra_kwargs = {
            "floor_plan": {"required": True},
            "gender": {"required": True},
        }

    def get_images(self, obj: Room):
        room_image = RoomImage.objects.filter(room=obj.id)

        return RoomImageSerializer(room_image, many=True).data

    def create(self, validated_data):
        images = validated_data.pop("images", [])

        instance = super().create(validated_data)
        self.create_or_update_attachment(instance, images)
        return instance

    def update(self, instance, validated_data):
        images = validated_data.pop("images", [])
        instance = super().update(instance, validated_data)
        self.create_or_update_attachment(instance, images)
        return instance

    def create_or_update_attachment(self, room, images):
        if images:
            RoomImage.objects.filter(room=room).delete()
            files_data = [
                {"room": room.id, "image": attachment} for attachment in images
            ]
            file_serializer = RoomImageSerializer(data=files_data, many=True)

            if file_serializer.is_valid(raise_exception=True):
                file_serializer.save()

    def to_representation(self, instance: RoomType):
        representation = super().to_representation(instance)

        representation["images"] = self.get_images(instance)

        return representation
