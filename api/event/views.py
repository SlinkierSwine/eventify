from typing import Any

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsAuthenticatedOrRetrieveListOnlyViewSet
from event.models import Event
from event.openapi import examples as openapi_examples
from event.openapi import responses as openapi_responses
from event.serializers import EventSerializer


@extend_schema_view(
    create=extend_schema(
        summary="Create new event",
        examples=openapi_examples.create_event_examples,
        responses=openapi_responses.create_event_responses,
    ),
    retrieve=extend_schema(
        summary="Get event by id",
        description="Available for not authenticated users",
        responses=openapi_responses.retrieve_event_responses,
    ),
    partial_update=extend_schema(
        summary="Update event",
        responses=openapi_responses.update_event_responses,
    ),
    list=extend_schema(
        summary="Get all user's event",
        responses=openapi_responses.retrieve_event_responses,
    ),
)
class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrRetrieveListOnlyViewSet,)

    def perform_create(self, serializer: EventSerializer):
        user = self.request.user
        return serializer.save(created_by=user)

    def list(self, request: Request, *args: Any, **kwargs: Any):
        user_id = kwargs["user_id"]
        queryset = self.get_queryset().filter(created_by__id=user_id)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
