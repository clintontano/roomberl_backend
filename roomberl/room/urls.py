from django.urls import path
from rest_framework import routers
from room.views import DuplicateRoomApiView
from room.views import RoomAmenityApiView
from room.views import RoomApiView
from room.views import RoomTypeApiView
from room.views import ViewRoomMembersApiView

app_name = "room"


router = routers.DefaultRouter()
router.register("amenities", RoomAmenityApiView, "amenities")
router.register("room_types", RoomTypeApiView, "room_types")
router.register("rooms", RoomApiView, "rooms")


urlpatterns = [
    path(
        "duplicate/<uuid:pk>/<int:quantity>/",
        DuplicateRoomApiView.as_view(),
        name="duplicate_room",
    ),
    path(
        "view-room-members/<uuid:room_id>/",
        ViewRoomMembersApiView.as_view(),
        name="view_room_members",
    ),
]

urlpatterns += router.urls
