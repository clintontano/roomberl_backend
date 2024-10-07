# serializers.py
from account.models import User
from account.models import UserAdditionalDetail
from account.serializers import SimpleUserAccountSerializer
from chats.models import Chat
from chats.models import ChatRoom
from core.serializers import CreatedByMixin
from crum import get_current_user
from django.db.models import OuterRef
from django.db.models import Subquery
from rest_framework import serializers


class ChatRoomSerializer(CreatedByMixin, serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            "id",
            "name",
            "participants",
            "created_by",
            "object_type",
            "display_name",
        ]
        extra_kwargs = {
            "created_by": {"required": False},
        }

    def get_participants(self, obj: ChatRoom):
        user_details = UserAdditionalDetail.objects.filter(user=OuterRef("pk")).values(
            "id", "nickname", "other_name"
        )

        return list(
            obj.participants.annotate(
                user_additional_detail_id=Subquery(user_details.values("id")),
                nickname=Subquery(user_details.values("nickname")),
                other_name=Subquery(user_details.values("other_name")),
            ).values(
                "id",
                "first_name",
                "last_name",
                "gender",
                "email",
                "mobile",
                "user_additional_detail_id",
                "nickname",
                "other_name",
            )
        )

    def get_display_name(self, obj: ChatRoom):
        user: User = get_current_user()

        if obj.object_type == Chat.OBJECT_TYPE.USER and user in obj.participants.all():
            other_participants = obj.participants.exclude(id=user.id)
            if other_participants.exists():
                other_user: User = other_participants.first()
                return other_user.get_full_name()

        return obj.name


class ChatReceiverMixin:
    pass


class ChatsSerializer(ChatReceiverMixin, serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    sender = SimpleUserAccountSerializer()
    room = ChatRoomSerializer()

    class Meta:
        model = Chat
        fields = "__all__"

    read_only_fields = ["id", "sender", "receiver", "room"]

    def get_children(self, obj: Chat):
        return ChatsSerializer(obj.get_children(), many=True).data


class ChatStartMessageSerializer(
    CreatedByMixin, ChatReceiverMixin, serializers.ModelSerializer
):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            "id",
            "content",
            "parent",
            "sender",
            "room",
            "object_type",
            "object_id",
        ]
        read_only_fields = [
            "id",
            "sender",
        ]
        extra_kwargs = {
            "content": {"required": True},
            "parent": {"required": False, "allow_null": True},
            "created_by": {"required": False},
            "sender": {"read_only": True},
        }

    def get_sender(self, obj: Chat):
        return SimpleUserAccountSerializer(obj.sender).data

    def get_room(self, obj: Chat):
        return ChatRoomSerializer(obj.room).data

    def to_representation(self, instance: Chat):
        representation = super().to_representation(instance)

        representation["room"] = self.get_room(instance)

        return representation


class CreateMessageSerializer(
    CreatedByMixin, ChatReceiverMixin, serializers.ModelSerializer
):
    sender = serializers.SerializerMethodField()
    object_type = serializers.SerializerMethodField()
    object_id = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            "content",
            "parent",
            "sender",
            "room",
            "object_type",
            "object_id",
            "children",
        ]
        read_only_fields = ["id", "sender", "room", "object_type", "object_id"]
        extra_kwargs = {
            "content": {"required": True},
            "parent": {"required": False, "allow_null": True},
            "created_by": {"required": False},
            "sender": {"read_only": True},
        }

    def get_object_type(self, obj: Chat):
        return obj.object_type

    def get_object_id(self, obj: Chat):
        return obj.object_id

    def get_sender(self, obj: Chat):
        return SimpleUserAccountSerializer(obj.sender).data

    def get_children(self, obj: Chat):
        return ChatsSerializer(obj.get_children(), many=True).data


class GetChatsSerializer(ChatReceiverMixin, serializers.ModelSerializer):
    room = ChatRoomSerializer()
    chats = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ["chats", "room"]
        read_only_fields = ["id", "sender", "room"]

    def get_chats(self, obj: Chat):
        root_chats = Chat.objects.filter(room=obj.room, parent=None)
        return ChatsSerializer(root_chats, many=True).data
