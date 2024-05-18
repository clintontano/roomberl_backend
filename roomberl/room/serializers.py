from core.serializers import CreatedByMixin
from django.conf import settings
from rest_framework import serializers
from room.models import Room
from room.models import RoomImage


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ["id", "room", "image"]


class RoomSerializer(CreatedByMixin, serializers.ModelSerializer):
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

    def to_representation(self, instance: RoomImage):
        representation = super().to_representation(instance)

        representation["images"] = RoomImageSerializer(
            instance.roomimage_set, many=True
        ).data

        return representation
