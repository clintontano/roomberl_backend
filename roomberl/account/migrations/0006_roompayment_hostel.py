# Generated by Django 5.0.6 on 2024-07-31 10:57
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0005_useradditionaldetail_nickname"),
        ("literals", "0004_hostel_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="roompayment",
            name="hostel",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="literals.hostel",
            ),
        ),
    ]
