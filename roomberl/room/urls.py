from rest_framework import routers
from room.views import RoomApiView
from room.views import RoomPricingSerializerView

app_name = "room"


router = routers.DefaultRouter()
router.register("rooms", RoomApiView, "rooms")
router.register("room-pricing", RoomPricingSerializerView, "room_pricing")

urlpatterns = []

urlpatterns += router.urls
