from account.models import User
from chats.models import Chat
from chats.models import OBJECT_TYPE
from room.models import Hostel
from room.models import Room


class ChatService:
    def get_chat_participants(self, object_type: str, object_id: str):
        if object_type == OBJECT_TYPE.HOSTEL:
            hostel = Hostel.objects.get(id=object_id)
            return User.objects.filter(hostel=hostel)
        elif object_type == OBJECT_TYPE.ROOM:
            room = Room.objects.get(id=object_id)
            return User.objects.filter(room=room)
        elif object_type == OBJECT_TYPE.USER:
            return User.objects.filter(id__in=[object_id])
        else:  # Global chat
            return User.objects.all()

    def user_can_participate(
        self, user: User, object_type: str, object_id: str
    ) -> bool:
        if object_type == OBJECT_TYPE.USER:
            # Allow chat if the object_id is a valid user and not the sender themselves
            return (
                User.objects.filter(id=object_id).exists() and str(user.id) != object_id
            )
        elif object_type == OBJECT_TYPE.HOSTEL:
            # Check if user belongs to the hostel
            return user.hostel and str(user.hostel.id) == object_id
        elif object_type == OBJECT_TYPE.ROOM:
            # Check if user belongs to the room
            return user.room and str(user.room.id) == object_id
        else:
            return False  # Unknown object type

    def get_or_create_chat(sself, sender: User, object_type: str, object_id: str):
        chat = Chat.objects.filter(
            object_type=object_type, object_id=object_id, parent=None
        ).first()

        if not chat:
            chat = Chat.objects.create(
                object_type=object_type,
                object_id=object_id,
                sender=sender,
                receiver=None
                if object_type != OBJECT_TYPE.USER
                else User.objects.get(id=object_id),
            )

        return chat
