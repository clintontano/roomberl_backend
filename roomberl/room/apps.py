from django.apps import AppConfig


class RoomConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "room"

    def ready(self) -> None:
        from room.signals import init_singals

        init_singals
        return super().ready()
