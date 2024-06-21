from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from account.serializers import UserSerializer
from event.models import Event, EventParticipant
from event.services.event_service import EventService


class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = ("user", "anonymous_participant")


class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    participants = EventParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ("is_canceled",)

    def create(self, validated_data):
        with transaction.atomic():
            try:
                event = super().create(validated_data)
            except DjangoValidationError as e:
                raise serializers.ValidationError(e.error_dict)

            EventService.create_event_participants(event, [event.created_by])

        return event
