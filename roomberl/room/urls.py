from rest_framework import routers
from room.views import RoomApiView

app_name = "room"


router = routers.DefaultRouter()
router.register("rooms", RoomApiView, "rooms")


urlpatterns = []

urlpatterns += router.urls
