from core.models import BaseModel
from django.db import models

# Create your models here.


class BaseLiterals(BaseModel):
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class University(BaseLiterals):
    pass


class Hostel(BaseLiterals):
    pass


class Semester(BaseLiterals):
    pass


class Year(BaseLiterals):
    pass


class RoomType(BaseLiterals):
    pass
