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


class Hostel(BaseLiterals):
    code = models.CharField(max_length=200, null=True, blank=True, unique=True)
    owner_name = models.CharField(max_length=200, null=True)
    owner_email = models.EmailField(null=True)
    owner_phone = models.CharField(max_length=15, null=True)
    location = models.CharField(max_length=200, null=True)
    website = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        code = self.name.lower().replace(" ", "_")
        self.code = code

        return super().save()
