from account.models import User
from chats.models import Chat
from chats.serializers import CreateMessageSerializer
from chats.serializers import GetChatsSerialiser
from core.dependency_injection import service_locator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import OBJECT_TYPE


class ChatApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Chat.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateMessageSerializer
        return GetChatsSerialiser

    def perform_create(self, serializer):
        object_type = self.request.data.get("object_type")
        object_id = self.request.data.get("object_id")
        parent_id = self.request.data.get("parent")

        if not service_locator.chat_service.user_can_participate(
            self.request.user, object_type, object_id
        ):
            raise PermissionDenied("You don't have permission to chat in this context.")

        try:
            parent = None
            if parent_id:
                parent = Chat.objects.get(id=parent_id)

            receiver = None
            if object_type == OBJECT_TYPE.USER:
                receiver = User.objects.get(id=object_id)

            serializer.save(
                sender=self.request.user,
                receiver=receiver,
                parent=parent,
                object_type=object_type,
                object_id=object_id,
            )
        except ObjectDoesNotExist as e:
            print(f"ObjectDoesNotExist error: {str(e)}")
            raise serializers.ValidationError(
                "Invalid object_id, parent_id, or user not found."
            )
        except Exception as e:
            print(f"Unexpected error in perform_create: {str(e)}")
            raise serializers.ValidationError(
                "An unexpected error occurred while creating the chat."
            )

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(
            Q(sender=user)
            | Q(receiver=user)
            | Q(
                object_id__in=[
                    chat.object_id for chat in Chat.objects.filter(sender=user)
                ]
            )
            | Q(
                object_type__in=[
                    chat.object_type for chat in Chat.objects.filter(sender=user)
                ]
            )
        ).distinct()

    @action(detail=False, methods=["get"])
    def get_chats(self, request):
        object_type = request.query_params.get("object_type")
        object_id = request.query_params.get("object_id")

        if not service_locator.chat_service.user_can_participate(
            request.user, object_type, object_id
        ):
            raise PermissionDenied("You don't have permission to view this chat.")

        chats = Chat.objects.filter(object_type=object_type, object_id=object_id)

        serializer = GetChatsSerialiser(chats, many=True)
        return Response(serializer.data)
