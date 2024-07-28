from chats import views
from django.urls import path

urlpatterns = [
    path("rooms-list/", views.ChatRoomsListApiView.as_view(), name="chat-start"),
    path("rooms-update/", views.ChatRoomsUpdateApiView.as_view(), name="chat-start"),
    path("start/", views.ChatStartApiView.as_view(), name="chat-start"),
    path(
        "create/<uuid:room_id>/",
        views.ChatCreateByRoomApiView.as_view(),
        name="chat-create",
    ),
    path("<uuid:room_id>/", views.ChatListApiView.as_view(), name="chat-list"),
    path(
        "<uuid:pk>/",
        views.ChatRetrieveUpdateDestroyApiView.as_view(),
        name="chat-detail",
    ),
]
