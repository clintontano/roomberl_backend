from account.models import CustomPermission
from account.models import Pair
from account.models import RoomPayment
from account.models import User
from account.models import UserAdditionalDetail
from core.dependency_injection import service_locator
from core.serializers import BaseRoomBerlSerializer
from core.serializers import BaseToRepresentation
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.encoding import force_bytes
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from literals.serializers import Hostel
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "content_type": {"read_only": True},
            "codename": {"read_only": True},
        }

    def create(self, validated_data):
        content_type = ContentType.objects.get_for_model(CustomPermission).id

        name = validated_data.get("name")
        codename = validated_data.get("name").lower()

        custom_permission = Permission.objects.create(
            codename=codename.replace(" ", "_").lower(),
            name=name,
            content_type_id=content_type,
        )

        return custom_permission


class GroupsSerializer(serializers.ModelSerializer):
    permissions_obj = PermissionSerializer(
        many=True, read_only=True, source="permissions"
    )

    class Meta:
        model = Group
        fields = ["id", "name", "permissions", "permissions_obj"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "pk": {"read_only": True},
            "permissions": {"write_only": True, "required": True},
        }


class SimpleUserAccountSerializer(serializers.ModelSerializer):
    groups = GroupsSerializer(many=True)
    hostel = serializers.SerializerMethodField()
    additional_details = serializers.SerializerMethodField()
    room_payments = serializers.SerializerMethodField()
    match_percentage = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "mobile",
            "address",
            "gender",
            "is_active",
            "groups",
            "hostel",
            "image",
            "additional_details",
            "room_payments",
            "match_percentage",
        ]

    def get_hostel(self, obj: User):
        if not obj.hostel:
            return
        return Hostel.objects.filter(id=obj.hostel.id).values()

    def get_additional_details(self, obj: User):
        return UserAdditionalDetail.objects.filter(user=obj).values()

    def get_room_payments(self, obj):
        room_paymens = RoomPayment.objects.filter(user=obj).order_by("user")

        return RoomPaymentSerializer(room_paymens, many=True).data

    def get_match_percentage(self, obj: User):
        if not hasattr(obj, "useradditionaldetail") or not obj.useradditionaldetail:
            return "0%"

        return service_locator.account_service.get_match_percentage(
            obj.useradditionaldetail
        )


class PairedUsersSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="id")

    class Meta:
        model = User
        fields = ["user_id", "email", "mobile", "address", "gender", "image", "hostel"]


class PairsSerializer(serializers.ModelSerializer):
    paired_users = PairedUsersSerializer(many=True, read_only=True)

    class Meta:
        model = Pair
        fields = ["paired_users"]


class UserAccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=False)
    groups_obj = GroupsSerializer(many=True, read_only=True, source="groups")
    match_percentage = serializers.SerializerMethodField()

    pairs = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all()),
        write_only=True,
        required=False,
        help_text="comma separated list of user ids",
    )

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["id", "is_superuser"]

        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True, "required": True},
            "is_superuser": {"read_only": True},
            "hostel": {"required": False},
        }

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = self.initial_data.get("password_2")

        if password and password2:
            if password != password2:
                raise serializers.ValidationError(
                    {"password2": "Password and Confirm Password do not match"}
                )
            try:
                validate_password(password)
            except ValidationError as e:
                raise serializers.ValidationError({"password": e.messages})

        return super().validate(attrs)

    def get_match_percentage(self, obj: User):
        if not hasattr(obj, "useradditionaldetail") or not obj.useradditionaldetail:
            return "0%"
        return service_locator.account_service.get_match_percentage(
            obj.useradditionaldetail
        )

    def get_pairs(self, obj: User):
        pairs = Pair.objects.filter(user=obj)
        return PairsSerializer(pairs, many=True).data

    @transaction.atomic
    def create(self, validated_data):
        pairs = validated_data.pop("pairs", [])

        instance = super().create(validated_data)

        Pair.objects.handle_pairs(instance, pairs)

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        pairs = validated_data.pop("pairs", [])

        instance = super().update(instance, validated_data)

        Pair.objects.handle_pairs(instance, pairs)

        return instance

    def to_representation(self, instance: User):
        representation = super().to_representation(instance)

        representation["pairs"] = self.get_pairs(instance)

        return representation


class UserTokenSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255,
        style={"input_type": "password"},
        write_only=True,
        required=False,
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = self.initial_data.get("password_2")
        user = self.context.get("user")
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match"
            )

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        user.set_password(password)
        user.save()
        return attrs


class BaseEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class SendResetSerializer(BaseEmailSerializer):
    pass


class SendPasswordResetEmailSerializer(BaseEmailSerializer):
    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")

        if User.objects.filter(email=email).exists():
            user: User = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            # Send EMail

            service_locator.core_service.send_email(
                subject=f"Reset Your Password for {user.email}",
                template_path="emails/password_reset_link.html",
                template_context={
                    "user": user,
                    "password_reset_link": f"{settings.FRONTEND_URL}/set-new-password/?uid={uid}&token={token}",
                    "body": "Click Following Link to Reset Your Password",
                },
                to_emails=[user.email],
            )
            return attrs
        else:
            raise serializers.ValidationError(
                code="user_account", detail="user account does not exist"
            )


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255,
        style={"input_type": "password"},
        write_only=True,
        required=False,
    )

    class Meta:
        fields = ["password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True, "required": True},
        }

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            password2 = self.initial_data.get("password_2")

            uid = self.context.get("uid")
            token = self.context.get("token")

            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password don't match"
                )

            user_id = smart_str(urlsafe_base64_decode(uid))
            user: User = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not Valid or Expired")

            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError("Token is not Valid or Expired")


class RoomPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPayment

        exclude = ["is_deleted"]

        read_only_fields = ["id"]

        extra_kwargs = {
            "pk": {"read_only": True},
            "room_type": {"required": True},
            "hostel": {"required": True},
        }

    def get_payment_status(self, obj: RoomPayment):
        total_paid = (
            RoomPayment.objects.filter(
                user=obj.user, room_type=obj.room_type, is_verified=True
            ).aggregate(total=Sum("amount_payed"))["total"]
            or 0
        )

        if total_paid >= obj.room_type.price:
            return "Full payment"
        elif total_paid > 0:
            return "Partial payment"
        else:
            return "No payment"

    def to_representation(self, instance: RoomPayment):
        serializer = BaseRoomBerlSerializer(instance=instance)
        serializer.Meta.model = instance.__class__
        serializer.Meta.depth = 1

        data = serializer.to_representation(instance)

        data["payment_status"] = self.get_payment_status(instance)

        return data


class UserAdditionalDetailSerializer(BaseToRepresentation, serializers.ModelSerializer):
    class Meta:
        model = UserAdditionalDetail
        exclude = ["is_deleted"]

    def get_room_payments(self, obj: UserAdditionalDetail):
        room_payments = RoomPayment.objects.filter(user=obj.user)
        return room_payments.values()

    def to_representation(self, instance: UserAdditionalDetail):
        representation = super().to_representation(instance)

        representation["room_payments"] = self.get_room_payments(instance)
        return representation

    def update(self, instance: UserAdditionalDetail, validated_data):
        room_type = validated_data.get("room_type", None)

        room = validated_data.get("room", None)
        if room_type:
            total_rooms = room_type.room_set.filter(is_locked=False).count()
            max_occupancy = total_rooms * room_type.num_occupancy
            current_occupancy = (
                RoomPayment.objects.filter(room_type=room_type, is_verified=True)
                .exclude(id=instance.id)
                .count()
            )

            if current_occupancy >= max_occupancy:
                raise serializers.ValidationError(
                    code="room_type_occupancy", detail="Room type is fully occupied"
                )

        if room and room.is_locked:
            raise serializers.ValidationError(
                code="room_locked", detail="this room is locked"
            )

        if room:
            num_occupancy: UserAdditionalDetail = UserAdditionalDetail.objects.filter(
                room=room
            ).count()

            if num_occupancy >= instance.room_type.num_occupancy:
                raise serializers.ValidationError(
                    code="num_occupancy", detail="this room is fully occupied"
                )

        return super().update(instance, validated_data)


class UserWithMatchesSerializer(serializers.ModelSerializer):
    user = SimpleUserAccountSerializer(read_only=True)

    class Meta:
        model = UserAdditionalDetail
        fields = [
            "id",
            "user",
            "nickname",
            "course_of_study",
            "profile_picture",
            "date_of_admission",
        ]


class ActivateUserAccountSerializer(serializers.Serializer):
    token = serializers.CharField()
