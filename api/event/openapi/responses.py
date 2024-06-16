from rest_framework import status

from core.openapi.responses import (
    OpenAPIResponsesDictType,
    default_responses,
    default_unauthorized_responses,
    not_found_responses,
)
from event.serializers import EventSerializer


create_event_responses: OpenAPIResponsesDictType = {
    **default_responses,
    status.HTTP_201_CREATED: EventSerializer,
}

retrieve_event_responses: OpenAPIResponsesDictType = {
    **default_unauthorized_responses,
    status.HTTP_200_OK: EventSerializer,
    **not_found_responses,
}

update_event_responses: OpenAPIResponsesDictType = {
    **default_unauthorized_responses,
    status.HTTP_200_OK: EventSerializer,
    **not_found_responses,
}

list_event_responses: OpenAPIResponsesDictType = {
    **default_responses,
    status.HTTP_200_OK: EventSerializer,
}