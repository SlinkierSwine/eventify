from typing import Any

from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from event.exceptions import EventException
from event.models import AnonymousParticipant, Event
from event.openapi import examples as openapi_examples
from event.openapi import responses as openapi_responses
from event.permissions import IsEventOwnerOrReadOnly
from event.serializers import AnonymousParticipantSerializer, EventSerializer
from event.services.event_service import EventService
from event.services.invitation_service import InvitationService


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
    destroy=extend_schema(
        summary="Delete event",
        responses=openapi_responses.retrieve_event_responses,
    ),
)
class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsEventOwnerOrReadOnly,)

    def get_object(self):
        obj = super().get_object()

        if obj.is_private and self.request.user != obj.created_by:
            raise EventException("Event is private")

        return obj

    def perform_create(self, serializer: EventSerializer):
        user = self.request.user
        return serializer.save(created_by=user)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user_id = kwargs["user_id"]
        filter_is_private = Q() if user_id == request.user.id else Q(is_private=False)
        queryset = self.get_queryset().filter(created_by__id=user_id).filter(filter_is_private)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


@extend_schema_view(
    post=extend_schema(
        summary="Add user to event's participants",
        responses=openapi_responses.add_user_participant_responses,
    )
)
class AddUserParticipantAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        event_id = self.kwargs["pk"]
        event = get_object_or_404(Event, pk=event_id)
        EventService.validate_not_canceled(event)
        EventService.validate_not_private(event)

        EventService.add_event_participant(event, request.user)

        return Response(status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        summary="User accepts invitation to event",
        responses=openapi_responses.add_user_participant_responses,
    )
)
class UserAcceptInvitationAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        uid = self.kwargs["uid"]
        event = InvitationService.get_event_from_uid(uid)
        EventService.validate_not_canceled(event)

        EventService.add_event_participant(event, request.user)

        return Response(status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        summary="Anonymos participant accepts invitation to event",
        responses=openapi_responses.anonymous_participant_accepts_invitation_responses,
    )
)
class AnonAcceptInvitationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AnonymousParticipantSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        uid = self.kwargs["uid"]
        event = InvitationService.get_event_from_uid(uid)
        EventService.validate_not_canceled(event)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(event=event)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
