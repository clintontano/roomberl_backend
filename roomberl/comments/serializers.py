from account.serializers import SimpleUserAccountSerializer
from comments.models import Comment
from core.serializers import CreatedByMixin
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    created_by = SimpleUserAccountSerializer()

    class Meta:
        model = Comment
        fields = "__all__"

    read_only_fields = ["id,created_by"]

    def get_children(self, obj: Comment):
        return CommentSerializer(obj.get_children(), many=True).data


class CreateCommentSerializer(CreatedByMixin, serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["id", "created_by"]
        extra_kwargs = {"content": {"required": True}}

    def to_representation(self, instance: Comment):
        representation = super().to_representation(instance)
        representation["created_by"] = SimpleUserAccountSerializer(
            instance.created_by
        ).data

        return representation


class GetCommetsSerialiser(serializers.ModelSerializer):
    chats = serializers.SerializerMethodField()
    created_by = SimpleUserAccountSerializer()

    class Meta:
        model = Comment
        fields = ["chats", "created_by"]
        read_only_fields = ["id", "created_by"]

    def get_chats(self, obj: Comment):
        root_chats = Comment.objects.filter(id=obj.id, parent=None)

        return CommentSerializer(root_chats, many=True).data
