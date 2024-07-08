from account.models import CustomPermission
from account.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction


def create_groups_and_assign_permissions():
    with transaction.atomic():
        # Create Administrator Group
        Group.objects.get_or_create(name=User.UserGroup.ADMINISTRATOR)

        content_type = ContentType.objects.get_for_model(CustomPermission)

        # Create Student group
        student_group, _ = Group.objects.get_or_create(name=User.UserGroup.STUDENT)

        # Create Hostel Manager group
        hostel_manager_group, _ = Group.objects.get_or_create(
            name=User.UserGroup.HOSTEL_MANAGER
        )

        # Define permissions for Student
        student_permissions = [
            "view_personality_profiles",
            "send_private_messages",
            "view_send_room_messages",
            "view_room_members",
            "view_room_info",
            "edit_self_profile",
            "reserve_bed_12hours",
        ]

        # Define permissions for Hostel Manager
        hostel_manager_permissions = [
            "manage_rooms",
            "manage_room_types",
            "create_student_accounts",
            "manage_room_assignments",
            "reserve_bed_24hours",
            "verify_payments",
            "view_personality_profiles",
            "send_private_messages",
            "view_room_messages",
            "review_roommate_matches",
            "lock_platforms",
        ]

        # Create and assign permissions to Student group
        for perm in student_permissions:
            permission, created = Permission.objects.get_or_create(
                codename=perm,
                name=perm.replace("_", " ").capitalize(),
                content_type=content_type,
            )
            student_group.permissions.add(permission)

        # Create and assign permissions to Hostel Manager group
        for perm in hostel_manager_permissions:
            permission, created = Permission.objects.get_or_create(
                codename=perm,
                name=perm.replace("_", " ").capitalize(),
                content_type=content_type,
            )
            hostel_manager_group.permissions.add(permission)

        print("Groups created and permissions assigned successfully.")


create_groups_and_assign_permissions()
