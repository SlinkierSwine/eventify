import logging

from django.contrib.auth.base_user import AbstractBaseUser

from event.exceptions import EventException
from event.models import AnonymousParticipant, Event, EventParticipant

logger = logging.getLogger(__name__)


class EventService:
    @classmethod
    def add_event_participant(
        cls,
        event: Event,
        participant: AbstractBaseUser | AnonymousParticipant,
    ) -> None:
        if isinstance(participant, AbstractBaseUser):
            event_participant, created = EventParticipant.objects.get_or_create(
                event=event, user=participant
            )

        elif isinstance(participant, AnonymousParticipant):
            event_participant, created = EventParticipant.objects.get_or_create(
                event=event, anonymous_participant=participant
            )

        else:
            raise EventException(
                "Event participant can be only user or anonymous participant"
            )

        if not created:
            raise EventException(f"{participant} is already participating in {event}")

        event.participants.add(event_participant)
        logger.info(
            f"{participant} is now participating in {event} ({event_participant})"
        )

    @classmethod
    def validate_not_canceled(cls, event: Event) -> None:
        if event.is_canceled:
            raise EventException("Event is canceled")

    @classmethod
    def validate_not_private(cls, event: Event) -> None:
        if event.is_private:
            raise EventException("Event is private")

    @classmethod
    def validate_anon_is_already_participating(
        cls, event: Event, anon: AnonymousParticipant
    ) -> None:
        if EventParticipant.objects.filter(
            anonymous_participant__notification_provider=anon.notification_provider,
            anonymous_participant__social_contact=anon.social_contact,
        ).exists():
            raise EventException(f"{anon} is already participating in {event}")
