# Generated by Django 5.0.6 on 2024-05-19 14:47
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0006_user_hostel_roompayment"),
        ("literals", "0003_hostel_semester_year"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={},
        ),
        migrations.AlterUniqueTogether(
            name="user",
            unique_together={("email", "hostel")},
        ),
    ]
