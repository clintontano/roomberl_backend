from django.urls import include
from django.urls import path

app_name = "api"

urlpatterns = [
    path("literals/", include("literals.urls")),
    path("accounts/", include("account.urls")),
    path("question/", include("question.urls")),
    path("room/", include("room.urls")),
]
