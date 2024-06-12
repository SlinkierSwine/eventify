from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.views import APIView, Request
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.serializers import RegistrationSerializer
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
        description="Password length must be between 9 and 128 characters",
        examples=openapi_examples.login_examples,
        responses=openapi_responses.login_responses,
    )
)
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
