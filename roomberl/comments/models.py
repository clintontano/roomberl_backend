from account.models import User
from core.models import BaseModel
from core.models import OBJECT_TYPE
from django.db import models
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey

# Create your models here.


class Comment(BaseModel, MPTTModel):
    content = models.TextField(null=True)
    object_id = models.UUIDField()
    object_type = models.CharField(max_length=200, choices=OBJECT_TYPE.CHOICES)

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ["created_at"]

    def __str__(self) -> str:
        return self.content

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the super() save method first
        # send email notification
