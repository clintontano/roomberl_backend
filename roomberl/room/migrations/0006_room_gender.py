# Generated by Django 5.0.6 on 2024-07-13 20:51
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("room", "0005_remove_room_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="gender",
            field=models.CharField(
                choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
                max_length=20,
                null=True,
            ),
        ),
    ]
