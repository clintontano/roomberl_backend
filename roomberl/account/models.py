import uuid
from datetime import datetime

from core.models import BaseModel
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db import transaction
from django.db.models.query import QuerySet
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext as _
from literals.models import Hostel
from literals.models import Institution
from rest_framework.exceptions import ValidationError


class UserManager(BaseUserManager):

    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().order_by("email")

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        if not email:
            raise ValueError(_("The Email must be set"))
        if not password:
            raise ValueError(_("The Password must be set"))
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        # groups = extra_fields.pop("groups", None)
        # user_permissions = extra_fields.pop("user_permissions", None)
        user: User = self.model(email=email, **extra_fields)
        # user.groups.set(groups)
        # user.user_permissions.set(user_permissions)
        user.set_password(password)
        user.is_active = True

        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    objects: UserManager = UserManager()
    useradditionaldetail: "UserAdditionalDetail"
    roompayment_set: "RoomPayment"

    class Gender:
        MALE = "Male"
        FEMALE = "Female"
        OTHER = "Other"

        CHOICES = (
            (MALE, _("Male")),
            (FEMALE, _("Female")),
            (OTHER, _("Other")),
        )

    class UserGroup:
        STUDENT = "Student"
        HOSTEL_MANAGER = "Hostel_manager"
        ADMINISTRATOR = "Administrator"

        CHOICES = (
            (STUDENT, _("Student")),
            (HOSTEL_MANAGER, _("Hostel Manager")),
            (ADMINISTRATOR, _("Administrator")),
        )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # noqa
    username = models.CharField(_("username"), max_length=255, blank=True, null=True)

    email = models.EmailField(_("user email"), max_length=254, unique=True)
    mobile = models.CharField(_("mobile number"), max_length=20, blank=True)
    address = models.CharField(_("address"), max_length=255, blank=True)

    gender = models.CharField(
        max_length=10, choices=Gender.CHOICES, default=Gender.OTHER
    )
    image = models.ImageField(upload_to="users", blank=True, null=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.PROTECT, null=True, blank=True)

    objects: UserManager = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name or self.last_name
            else self.email
        )

    @property
    def full_name(self):
        return self.__str__()


@receiver(post_save, sender=User)
def create_user_role(sender, instance: User, created, **kwargs):
    if created:
        group = Group.objects.filter(name=User.UserGroup.STUDENT).first()
        if not group:
            return

        if not instance.groups.exists():
            instance.groups.add(group)


class CustomPermission(models.Model):
    """THIS IS A MODEL FOR CUSTOM PERMISSIONS BASED ON content_type"""


class UserAdditionalDetail(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    other_name = models.CharField(max_length=200, null=True, blank=True)
    nickname = models.CharField(max_length=200, null=True, blank=True)
    guardian_full_name = models.CharField(max_length=200, null=True, blank=True)
    ghana_card_number = models.CharField(max_length=15, null=True, blank=True)
    course_of_study = models.CharField(max_length=200, null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True)
    admission_picture = models.ImageField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)
    pictur_of_ghana_card = models.ImageField(blank=True, null=True)
    student_id_number = models.CharField(max_length=20, null=True, blank=True)
    date_of_admission = models.DateField(null=True, blank=True)
    responses = models.JSONField(default=dict, blank=True)
    room = models.ForeignKey(
        "room.room", null=True, on_delete=models.SET_NULL, blank=True
    )
    room_type = models.ForeignKey(
        "room.roomtype", on_delete=models.SET_NULL, blank=True, null=True
    )

    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, null=True, blank=True
    )
    course_level = models.CharField(max_length=200, blank=True, null=True)


class RoomPayment(BaseModel):
    class STATUS:
        VERIFIED = "verified"
        REJECTED = "rejected"
        NOT_VERIFIED = "not_verified"

        ALL = (VERIFIED, REJECTED, NOT_VERIFIED)

        CHOICES = (
            (VERIFIED, ("Verified")),
            (REJECTED, ("Rejected")),
            (NOT_VERIFIED, ("Not Verified")),
        )

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    room_type = models.ForeignKey("room.roomtype", on_delete=models.SET_NULL, null=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, null=True)
    amount_payed = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True)
    first_receipt = models.ImageField(blank=True)
    second_receipt = models.ImageField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=STATUS.CHOICES, default=STATUS.NOT_VERIFIED
    )

    def save(self, *args, **kwargs):
        if (
            self.hostel
            and self.hostel.dead_line
            and self.hostel.dead_line < timezone.now().date()
        ):
            raise ValidationError(
                code="deadline",
                detail="Payment cannot be made after the deadline for this hostel.",
            )

        self.check_payment_status()
        super().save(*args, **kwargs)

    def check_payment_status(self):
        if self.is_verified:
            self.status = self.STATUS.VERIFIED

        if not self.is_verified:
            self.status = self.STATUS.NOT_VERIFIED


@receiver(post_save, sender=RoomPayment)
@transaction.atomic
def send_payment_verification(sender, instance: RoomPayment, created, **kwargs):
    from core.dependency_injection import service_locator

    now = datetime.now()
    hostel = instance.user.hostel
    if created and hostel.owner_email:
        service_locator.core_service.send_email(
            subject="Payment Made",
            template_path="emails/payment_created.html",
            template_context={
                "hostel_owner": hostel.owner_name,
                "student": instance.user.full_name,
                "room_type": instance.room_type.name,
                "hostel": hostel.name,
                "created_at": instance.created_at,
                "amount_payed": instance.amount_payed,
                "today": now.strftime("%A %B %d %I %p"),
            },
            to_emails=[hostel.owner_email],
        )

    if instance.is_verified:
        service_locator.core_service.send_email(
            subject="Payment Verification",
            template_path="emails/payment_verification.html",
            template_context={
                "student": instance.user.full_name,
                "room_type": instance.room_type.name,
                "hostel": hostel.name,
                "created_at": instance.created_at,
                "amount_payed": instance.amount_payed,
                "today": now.strftime("%A %B %d %I %p"),
            },
            to_emails=[instance.user.email],
        )


class PairsManager(models.Manager):
    def handle_pairs(self, instance, pairs_data):
        pair_instance, created = self.get_or_create(user=instance)
        pair_instance: Pair

        if pairs_data is not None:
            pair_instance.paired_users.set(pairs_data)

        else:
            pair_instance.paired_users.clear()

        return pair_instance


class Pair(BaseModel):
    objects: PairsManager = PairsManager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paired_users = models.ManyToManyField(User, related_name="+")


@receiver(m2m_changed, sender=Pair.paired_users.through)
def send_pairing_email(
    sender, instance: Pair, action, reverse, model: Pair, pk_set, **kwargs
):
    if action == "post_add":  # or action == 'post_remove':
        users = model.objects.filter(pk__in=pk_set)

        for user in users:
            user: User

            message = (
                "Dear {}, you have been added as a new pair by {} on RoomBerl.".format(
                    user.full_name, instance.user.full_name
                )
            )
            send_pairing_notification(user, message)


def send_pairing_notification(user: User, message: str):
    from core.dependency_injection import service_locator

    subject = "Your Pairing Status has Changed"

    service_locator.core_service.send_email(
        subject=subject,
        template_path="emails/paired_users.html",
        template_context={
            "user": user,
            "message": message,
        },
        to_emails=[user.email],
    )
