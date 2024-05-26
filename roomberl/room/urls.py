from rest_framework import routers
from room.views import RoomAmenityApiView
from room.views import RoomApiView
from room.views import RoomTypeApiView

app_name = "room"


router = routers.DefaultRouter()
router.register("amenities", RoomAmenityApiView, "amenities")
router.register("room_types", RoomTypeApiView, "room_types")
router.register("rooms", RoomApiView, "rooms")


urlpatterns = []

urlpatterns += router.urls
