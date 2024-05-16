from literals.views import ListLiteralsView
from django.urls import path

app_name = "literals"

urlpatterns = [
    path('all/', ListLiteralsView.as_view(), name='all_literals'),
]
