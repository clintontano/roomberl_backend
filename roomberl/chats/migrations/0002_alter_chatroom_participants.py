# Generated by Django 5.0.6 on 2024-07-29 18:22
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("chats", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatroom",
            name="participants",
            field=models.ManyToManyField(
                blank=True, related_name="chat_rooms", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
