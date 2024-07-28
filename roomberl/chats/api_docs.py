from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

CHATS_SWAGGER_DOCS = swagger_auto_schema(
    operation_description="Filter by Room ID",
    responses={},
    manual_parameters=[
        openapi.Parameter(
            "room_id",
            openapi.IN_QUERY,
            description="ROOM ID",
            type=openapi.TYPE_STRING,
        ),
    ],
)
