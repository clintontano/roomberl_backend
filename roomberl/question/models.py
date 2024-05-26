from core.models import BaseModel
from django.db import models


class Category(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Question(BaseModel):
    text = models.TextField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.text} {self.category.name}"


class Option(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    chosen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} {self.question.text} {self.chosen}"

    class Meta:
        ordering = ["created_at"]
