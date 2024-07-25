from chats.views import ChatApiView
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", ChatApiView, basename="chats")

urlpatterns = [
    path("", include(router.urls)),
]
