from django.apps import AppConfig


class LiteralsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "literals"

    def ready(self) -> None:
        return super().ready()
