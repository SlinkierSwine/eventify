from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.views import APIView, Request

from account.serializers import LoginSerializer, RegistrationSerializer, UserSerializer
import account.openapi.responses as openapi_responses
import account.openapi.examples as openapi_examples


@extend_schema_view(
    post=extend_schema(
        summary="Create new user with given unique email",
        description="Password length must be between 9 and 128 characters",
        examples=openapi_examples.registration_examples,
        responses=openapi_responses.registration_responses,
    )
)
class RegistrationAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Login user if exists",
        description="Password length must be between 8 and 128 characters",
        examples=openapi_examples.login_examples,
        responses=openapi_responses.login_responses,
    )
)
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve current user",
        responses=openapi_responses.get_current_user_responses,
    ),
    put=extend_schema(
        exclude=True,
    ),
    patch=extend_schema(
        summary="Partially update current user",
        responses=openapi_responses.partially_update_current_user_responses,
    ),
)
class CurrentUserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permissions = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
