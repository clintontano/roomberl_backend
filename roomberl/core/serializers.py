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
