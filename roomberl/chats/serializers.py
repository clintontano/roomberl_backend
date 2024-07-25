from account.serializers import SimpleUserAccountSerializer
from chats.models import Chat
from rest_framework import serializers


class ChatsSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    sender = SimpleUserAccountSerializer()
    receiver = SimpleUserAccountSerializer()

    class Meta:
        model = Chat
        fields = "__all__"

    read_only_fields = ["id", "sender", "receiver"]

    def get_children(self, obj: Chat):
        return ChatsSerializer(obj.get_children(), many=True).data


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["content", "object_type", "object_id", "parent", "sender", "receiver"]
        read_only_fields = ["id", "sender", "receiver"]
        extra_kwargs = {
            "content": {"required": True},
            "object_type": {"required": True},
            "object_id": {"required": True},
            "parent": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance: Chat):
        representation = super().to_representation(instance)
        representation["sender"] = SimpleUserAccountSerializer(instance.sender).data
        if instance.receiver:
            representation["receiver"] = SimpleUserAccountSerializer(
                instance.receiver
            ).data
        return representation


class GetChatsSerialiser(serializers.ModelSerializer):
    chats = serializers.SerializerMethodField()
    sender = SimpleUserAccountSerializer()

    class Meta:
        model = Chat
        fields = ["chats", "sender", "receiver", "object_type", "object_id"]
        read_only_fields = ["id", "sender", "receiver"]

    def get_chats(self, obj: Chat):
        root_chats = Chat.objects.filter(object_id=obj.object_id, parent=None)

        return ChatsSerializer(root_chats, many=True).data
