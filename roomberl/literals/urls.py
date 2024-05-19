from django.urls import path
from literals.views import ListLiteralsView
from literals.views import UnauthenticatedListLiteralsView

app_name = "literals"

urlpatterns = [
    path("all/", ListLiteralsView.as_view(), name="all_literals"),
    path(
        "Unauthenticated/",
        UnauthenticatedListLiteralsView.as_view(),
        name="Unauthenticated",
    ),
]
