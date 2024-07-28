# models.py
from account.models import User
from core.models import BaseModel
from core.models import OBJECT_TYPE
from django.db import models
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey


class ChatRoom(BaseModel):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name="chat_rooms")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name",)


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
