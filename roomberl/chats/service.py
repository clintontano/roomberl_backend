from account.models import User
from chats.models import ChatRoom
from chats.models import OBJECT_TYPE
from django.core.exceptions import ObjectDoesNotExist
from room.models import Hostel


class ChatService:
    def get_chat_participants(self, object_type: str, object_id: str):
        try:
            if object_type == OBJECT_TYPE.HOSTEL:
                hostel = Hostel.objects.get(id=object_id)
                return User.objects.filter(hostel=hostel)
            elif object_type == OBJECT_TYPE.ROOM:
                return User.objects.filter(useradditionaldetail__room_id=object_id)
            elif object_type == OBJECT_TYPE.USER:
                return User.objects.filter(id=object_id)
            else:
                return User.objects.none()
        except ObjectDoesNotExist:
            return User.objects.none()

    def user_can_participate(self, user: User, room: ChatRoom) -> bool:
        return room.participants.filter(id=user.id).exists()

    def get_or_create_room(
        self, user: User, name: str, object_type: str, object_id: str
    ) -> ChatRoom:
        room, created = ChatRoom.objects.get_or_create(
            created_by=user, defaults={"name": name}
        )
        if created:
            participants = self.get_chat_participants(object_type, object_id)
            room.participants.set(participants)
            room.participants.add(user)
        return room
