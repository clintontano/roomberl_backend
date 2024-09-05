from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


MATCHING_USERS_SWAGGER_DOCS = swagger_auto_schema(
    operation_description="Filter by hostels",
    responses={},
    manual_parameters=[
        openapi.Parameter(
            "hostel",
            openapi.IN_QUERY,
            description="hostel",
            type=openapi.TYPE_STRING,
        ),
    ],
)
