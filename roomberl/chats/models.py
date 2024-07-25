from account.models import User
from core.models import BaseModel
from core.models import OBJECT_TYPE
from django.db import models
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey

# Create your models here.


class Chat(BaseModel, MPTTModel):
    content = models.TextField(null=True)
    object_id = models.UUIDField()
    object_type = models.CharField(max_length=200, choices=OBJECT_TYPE.CHOICES)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_chats"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_chats",
        null=True,
        blank=True,
    )

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    class MPTTMeta:
        order_insertion_by = ["created_at"]

    @property
    def is_group_chat(self):
        return self.object_type in [OBJECT_TYPE.HOSTEL, OBJECT_TYPE.ROOM]
