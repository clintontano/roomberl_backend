from django.db import models
from core.models import BaseModel
# Create your models here.

from django_better_admin_arrayfield.models.fields import ArrayField


class BaseLiterals(BaseModel):
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class University(BaseLiterals):
    pass
