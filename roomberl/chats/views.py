from chats.models import Chat
from chats.models import ChatRoom
from chats.serializers import ChatRoomSerializer
from chats.serializers import ChatStartMessageSerializer
from chats.serializers import CreateMessageSerializer
from chats.serializers import GetChatsSerializer
from core.dependency_injection import service_locator
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated


class ChatRoomsListApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer
    queryset = ChatRoom.objects.all()
    filterset_fields = ["object_type"]

    def get_queryset(self):
        user = self.request.user

        public_rooms = ChatRoom.objects.filter(object_type=ChatRoom.OBJECT_TYPE.PUBLIC)

        user_rooms = ChatRoom.objects.filter(participants=user)

        queryset = user_rooms | public_rooms

        return queryset.order_by("-created_at")


class ChatRoomsUpdateApiView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer
    queryset = ChatRoom.objects.order_by("-created_at")


class ChatStartApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatStartMessageSerializer

    def perform_create(self, serializer):
        user = self.request.user
        object_type = self.request.data.get("object_type")
        object_id = self.request.data.get("object_id")
        parent_id = self.request.data.get("parent")

        chat_room = get_object_or_404(ChatRoom, id=self.request.data.get("room"))

        service_locator.chat_service.create_chat_participants(
            user, chat_room, object_type, object_id
        )

        if not service_locator.chat_service.user_can_participate(user, chat_room):
            raise PermissionDenied("You don't have permission to chat in this room.")

        serializer.is_valid(raise_exception=True)

        serializer.save(
            sender=user,
            parent_id=parent_id,
            room=chat_room,
        )


class ChatCreateByRoomApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateMessageSerializer

    def perform_create(self, serializer):
        user = self.request.user
        room_id = self.kwargs.get("room_id")
        parent_id = self.request.data.get("parent")

        room = get_object_or_404(ChatRoom, id=room_id)

        chat = parent = Chat.objects.filter(room=room_id).first()

        if not chat:
            raise ValidationError(code="chat", detail="chat with room not found")
        serializer.validated_data.update(
            {"object_id": chat.object_id, "object_type": chat.object_type}
        )

        if not service_locator.chat_service.user_can_participate(user, room):
            raise PermissionDenied("You don't have permission to chat in this room.")

        parent = None
        if parent_id:
            try:
                parent = Chat.objects.get(id=parent_id)
            except Chat.DoesNotExist:
                raise ValidationError(code="Parent ID", detail="Parent chat not found.")

        serializer.save(
            sender=user,
            parent=parent,
            room=room,
        )


class ChatListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetChatsSerializer

    def get_queryset(self):
        room_id = self.kwargs.get("room_id")

        room = get_object_or_404(ChatRoom, id=room_id)

        if not service_locator.chat_service.user_can_participate(
            self.request.user, room
        ):
            raise PermissionDenied("You don't have permission to view this chat.")

        return Chat.objects.filter(room=room).order_by("created_at")


class ChatRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Chat.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return CreateMessageSerializer
        return GetChatsSerializer

    def get_queryset(self):
        object_type = self.request.query_params.get("object_type")
        object_id = self.request.query_params.get("object_id")

        if not object_type or not object_id:
            raise ValidationError(
                code="object_type or object_id",
                detail="Both object_type and object_id must be provided.",
            )

        room_name = f"{object_type}_{object_id}"
        try:
            room = ChatRoom.objects.get(name=room_name)
        except ChatRoom.DoesNotExist:
            raise ValidationError(code="room", detail="Room not found.")

        if not service_locator.chat_service.user_can_participate(
            self.request.user, room
        ):
            raise PermissionDenied("You don't have permission to view this chat.")

        return Chat.objects.filter(room=room).order_by("created_at")
