from account.models import RoomPayment
from account.models import User
from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = [
            "id",
            "hostel",
            "email",
        ]


class RoomPaymentFilter(filters.FilterSet):
    class Meta:
        model = RoomPayment
        fields = [
            "id",
            "hostel",
            "room_type",
            "user",
        ]
