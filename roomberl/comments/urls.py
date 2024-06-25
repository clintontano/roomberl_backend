from comments.views import CommentApiView
from rest_framework import routers

app_name = "comments"

router = routers.DefaultRouter()
router.register("", CommentApiView, "comments")


urlpatterns = []

urlpatterns += router.urls
