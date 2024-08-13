from django.urls import path
from rest_framework import routers
from room.views import DuplicateRoomApiView
from room.views import RoomAmenityApiView
from room.views import RoomApiView
from room.views import RoomTypeApiView

app_name = "room"


router = routers.DefaultRouter()
router.register("amenities", RoomAmenityApiView, "amenities")
router.register("room_types", RoomTypeApiView, "room_types")
router.register("rooms", RoomApiView, "rooms")


urlpatterns = [
    path(
        "duplcate/<uuid:pk>/<int:quantity>/",
        DuplicateRoomApiView.as_view(),
        name="duplicate_room",
    ),
]

urlpatterns += router.urls
