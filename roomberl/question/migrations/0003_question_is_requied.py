# Generated by Django 5.0.6 on 2024-07-08 11:25
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("question", "0002_alter_option_options_alter_question_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="is_requied",
            field=models.BooleanField(default=False),
        ),
    ]
