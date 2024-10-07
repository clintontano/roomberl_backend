# models.py
from account.models import User
from account.models import UserAdditionalDetail
from core.models import BaseModel
from core.models import OBJECT_TYPE
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey


class ChatRoom(BaseModel):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name="chat_rooms", blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    object_type = models.CharField(
        max_length=255, choices=OBJECT_TYPE.CHOICES, default=OBJECT_TYPE.PUBLIC
    )


class Chat(BaseModel, MPTTModel):
    object_type = models.CharField(max_length=255, choices=OBJECT_TYPE.CHOICES)
    object_id = models.UUIDField()
    content = models.TextField(null=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_chats"
    )

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="chats")

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ["created_at"]

    @property
    def is_group_chat(self):
        return self.room is not None


@receiver(post_save, sender=User)
def add_user_to_hostel_participants(sender, instance: User, created: bool, **kwargs):
    if created and hasattr(instance, "hostel") and instance.hostel:
        chats = Chat.objects.filter(object_id=instance.hostel.id)
        if not chats:
            return
        for chat in chats:
            chat.room.participants.add(instance)


@receiver(post_save, sender=UserAdditionalDetail)
def add_user_to_room_participants(
    sender, instance: UserAdditionalDetail, created: bool, **kwargs
):
    if hasattr(instance, "room") and instance.room:
        chats = Chat.objects.filter(object_id=instance.room.id)

        if not chats:
            return
        for chat in chats:
            chat.room.participants.add(instance.user)
