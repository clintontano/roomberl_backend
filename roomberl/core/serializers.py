from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response


class CreatedByMixin:
    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return super().create(validated_data)


class SoftDeleteMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Set is_deleted to True instead of deleting the object
        instance.is_deleted = True
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseRoomBerlSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        exclude = [
            "is_deleted",
        ]
        depth = 1


class BaseToRepresentation:
    def to_representation(self, instance):
        serializer = BaseRoomBerlSerializer(instance=instance)
        serializer.Meta.model = instance.__class__
        return serializer.data if instance else {}
