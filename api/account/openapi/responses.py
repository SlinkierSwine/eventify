from rest_framework import status

from account.serializers import LoginSerializer, RegistrationSerializer
from core.openapi.responses import OpenAPIResponsesDictType
from core.openapi.responses import (
    OpenAPIResponsesDictType,
    default_unauthorized_responses,
)


registration_responses: OpenAPIResponsesDictType = {
    **default_unauthorized_responses,
    status.HTTP_201_CREATED: RegistrationSerializer,
}


login_responses: OpenAPIResponsesDictType = {
    **default_unauthorized_responses,
    status.HTTP_200_OK: LoginSerializer,
}