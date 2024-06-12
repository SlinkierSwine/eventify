from drf_spectacular.utils import OpenApiExample, OpenApiResponse
from rest_framework import serializers, status

OpenAPIResponsesDictType = dict[
    int, OpenApiResponse | type[serializers.Serializer] | serializers.Serializer | None
]


class DummyDetailSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()


class DummyDetailAndStatusSerializer(DummyDetailSerializer):
    detail = serializers.CharField()


default_unauthorized_responses: OpenAPIResponsesDictType = {
    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
        DummyDetailAndStatusSerializer(),
        examples=[
            OpenApiExample("Bad request", value={"statusCode": 400, "detail": "string"})
        ],
    ),
    status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
        DummyDetailAndStatusSerializer(),
        examples=[
            OpenApiExample(
                "Server error", value={"statusCode": 500, "detail": "string"}
            )
        ],
    ),
}

default_responses: OpenAPIResponsesDictType = {
    **default_unauthorized_responses,
    status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
        DummyDetailAndStatusSerializer(),
        examples=[
            OpenApiExample(
                "Unauthorized", value={"statusCode": 401, "detail": "string"}
            )
        ],
    ),
    status.HTTP_403_FORBIDDEN: OpenApiResponse(
        DummyDetailAndStatusSerializer(),
        examples=[
            OpenApiExample("Forbidden", value={"statusCode": 403, "detail": "string"})
        ],
    ),
}

not_found_responses: OpenAPIResponsesDictType = {
    status.HTTP_404_NOT_FOUND: OpenApiResponse(
        DummyDetailAndStatusSerializer(),
        examples=[
            OpenApiExample("Not found", value={"statusCode": 404, "detail": "string"})
        ],
    )
}
