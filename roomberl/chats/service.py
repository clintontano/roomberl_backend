import logging
import random

from account.models import User
from chats.models import ChatRoom
from chats.models import OBJECT_TYPE
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from faker import Faker
from room.models import Hostel

logger = logging.getLogger(__name__)


class ChatService:
    def get_chat_participants(self, object_type: str, object_id: str):
        try:
            if object_type == OBJECT_TYPE.HOSTEL:
                hostel = Hostel.objects.get(id=object_id)
                return User.objects.filter(hostel=hostel)
            elif object_type == OBJECT_TYPE.ROOM:
                return User.objects.filter(
                    useradditionaldetail__room_id=object_id
                ).distinct()
            elif object_type == OBJECT_TYPE.USER:
                return User.objects.filter(id=object_id)

            else:
                logger.warning(f"Invalid object_type: {object_type}")
                return User.objects.none()
        except ObjectDoesNotExist:
            logger.warning(
                f"Object not found for type {object_type} and id {object_id}"
            )
            return User.objects.none()

    def user_can_participate(self, user: User, room: ChatRoom) -> bool:
        return (
            room.participants.filter(id=user.id).exists()
            or room.object_type == ChatRoom.OBJECT_TYPE.PUBLIC
        )

    @transaction.atomic
    def create_chat_participants(
        self, user: User, room: ChatRoom, object_type: str, object_id: str
    ) -> User:
        if object_type == OBJECT_TYPE.PUBLIC:
            return

        participants = self.get_chat_participants(object_type, object_id)

        if not participants.exists():
            logger.warning(f"No participants found for {object_type} {object_id}")
            participants = User.objects.filter(id=user.id)
        else:
            participants = list(participants)

        room.participants.add(*participants)

    @property
    def generate_chat_room_name(self):
        fake = Faker()

        adjectives = [
            "Cozy",
            "Vibrant",
            "Friendly",
            "Lively",
            "Charming",
            "Peaceful",
            "Cheerful",
            "Warm",
            "Inviting",
            "Exciting",
            "Interesting",
            "Awesome",
        ]

        nouns = [
            "Lounge",
            "Hub",
            "Space",
            "Spot",
            "Corner",
            "Nook",
            "Room",
            "Zone",
            "Place",
            "Circle",
            "Hangout",
            "Retreat",
        ]

        patterns = [
            f"{random.choice(adjectives)} {random.choice(nouns)}",
            f"{fake.color_name().capitalize()} {random.choice(nouns)}",
        ]
        return random.choice(patterns)
