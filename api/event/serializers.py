from typing import Any
from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from account.serializers import UserSerializer
from event.models import AnonymousParticipant, Event, EventParticipant
from event.services.event_service import EventService
from event.services.invitation_service import InvitationService


class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = ("user", "anonymous_participant")


class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    participants = EventParticipantSerializer(many=True, read_only=True)
    invitation_link = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ("is_canceled",)

    def get_invitation_link(self, obj: Event) -> str:
        return InvitationService.get_invitation_link(obj)

    def create(self, validated_data: Any) -> Event:
        with transaction.atomic():
            try:
                event = super().create(validated_data)
            except DjangoValidationError as e:
                raise serializers.ValidationError(e.error_dict)

            EventService.add_event_participant(event, event.created_by)

        return event


class AnonymousParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousParticipant
        fields = "__all__"

    def create(self, validated_data: Any) -> AnonymousParticipant:
        event = validated_data.pop("event")
        anon, _ = AnonymousParticipant.objects.get_or_create(**validated_data)
        EventService.validate_anon_is_already_participating(event, anon)
        EventService.add_event_participant(event, anon)

        return anon
