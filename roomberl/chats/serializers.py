# serializers.py
from account.serializers import SimpleUserAccountSerializer
from chats.models import Chat
from chats.models import ChatRoom
from core.serializers import CreatedByMixin
from rest_framework import serializers


class ChatRoomSerializer(CreatedByMixin, serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = [
            "id",
            "name",
        ]
        extra_kwargs = {
            "created_by": {"required": False},
        }


class ChatsSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    sender = SimpleUserAccountSerializer()
    room = ChatRoomSerializer()

    class Meta:
        model = Chat
        fields = "__all__"

    read_only_fields = ["id", "sender", "receiver", "room"]

    def get_children(self, obj: Chat):
        return ChatsSerializer(obj.get_children(), many=True).data


class ChatStartMessageSerializer(CreatedByMixin, serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ["content", "parent", "sender", "room", "object_type", "object_id"]
        read_only_fields = [
            "id",
            "sender",
            "room",
        ]
        extra_kwargs = {
            "content": {"required": True},
            "parent": {"required": False, "allow_null": True},
            "created_by": {"required": False},
            "sender": {"read_only": True},
        }

    def get_sender(self, obj: Chat):
        return SimpleUserAccountSerializer(obj.sender).data


class CreateMessageSerializer(CreatedByMixin, serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    object_type = serializers.SerializerMethodField()
    object_id = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ["content", "parent", "sender", "room", "object_type", "object_id"]
        read_only_fields = ["id", "sender", "room", "object_type", "object_id"]
        extra_kwargs = {
            "content": {"required": True},
            "parent": {"required": False, "allow_null": True},
            "created_by": {"required": False},
            "sender": {"read_only": True},
        }

    def get_object_type(self, obj):
        return obj.room.name.split("_")[0] if obj.room else None

    def get_object_id(self, obj):
        return obj.room.name.split("_")[1] if obj.room else None

    def get_sender(self, obj: Chat):
        return SimpleUserAccountSerializer(obj.sender).data


class GetChatsSerializer(serializers.ModelSerializer):
    room = ChatRoomSerializer()
    chats = serializers.SerializerMethodField()
    # sender = SimpleUserAccountSerializer()

    class Meta:
        model = Chat
        fields = ["chats", "room"]
        read_only_fields = ["id", "sender", "room"]

    def get_chats(self, obj: Chat):
        root_chats = Chat.objects.filter(room=obj.room, parent=None)
        return ChatsSerializer(root_chats, many=True).data
