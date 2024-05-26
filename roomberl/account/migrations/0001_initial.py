# Generated by Django 5.0.6 on 2024-05-25 22:41
import uuid

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("literals", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomPermission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="username"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="user email"
                    ),
                ),
                (
                    "mobile",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="mobile number"
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="address"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Other", "Other"),
                        ],
                        default="Other",
                        max_length=10,
                    ),
                ),
                ("image", models.ImageField(blank=True, null=True, upload_to="users")),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "hostel",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="literals.hostel",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "unique_together": {("email", "hostel")},
            },
        ),
        migrations.CreateModel(
            name="UserAdditionalDetail",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("other_name", models.CharField(blank=True, max_length=200, null=True)),
                ("guardian_full_name", models.CharField(max_length=200)),
                (
                    "ghana_card_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                ("course_of_study", models.CharField(max_length=200)),
                (
                    "profile_picture",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                (
                    "admission_picture",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "guardian_phone",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "pictur_of_ghana_card",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                ("student_id_number", models.CharField(max_length=20)),
                ("date_of_admission", models.DateField()),
                ("responses", models.JSONField(blank=True, default=dict)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
