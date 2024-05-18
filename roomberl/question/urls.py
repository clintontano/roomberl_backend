from django.urls import path
from question.views import CategoryApiView

app_name = "question"

urlpatterns = [path("question/", CategoryApiView.as_view(), name="question")]
