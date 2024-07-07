from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


HOSTELS_SWAGGER_DOCS = swagger_auto_schema(
    operation_description="Filter hostels by unique  code ",
    responses={},
    manual_parameters=[
        openapi.Parameter(
            "code",
            openapi.IN_QUERY,
            description="code",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "name",
            openapi.IN_QUERY,
            description="name",
            type=openapi.TYPE_STRING,
        ),
    ],
)
