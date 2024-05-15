import uuid

from django.db import models


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    class STATUS:
        PENDING = "pending"
        REJECTED = "rejected"
        CLOSED = "closed"
        ACTIVE = "active"
        NOT_ACTIVE = "not_active"

        ALL = (PENDING, REJECTED, CLOSED, ACTIVE)

        CHOICES = (
            (PENDING, ("Pending")),
            (REJECTED, ("Rejected")),
            (CLOSED, ("Closed")),
            (ACTIVE, ("Active")),
            (NOT_ACTIVE, ("Not Active")),
        )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # noqa
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
