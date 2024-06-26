import logging

from django.contrib.auth.base_user import AbstractBaseUser

from event.exceptions import EventException
from event.models import AnonymousParticipant, Event, EventParticipant
from notification.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class EventService:
    @classmethod
    def add_event_participant(
        cls,
        event: Event,
        participant: AbstractBaseUser | AnonymousParticipant,
    ) -> None:
        if isinstance(participant, AbstractBaseUser):
            data = {"event": event, "user": participant}
        elif isinstance(participant, AnonymousParticipant):
            data = {"event": event, "anonymous_participant": participant}
        else:
            raise EventException(
                "Event participant can be only user or anonymous participant"
            )

        event_participant = cls._participate_or_error(data)

        event.participants.add(event_participant)
        logger.info(
            f"{participant} is now participating in {event} ({event_participant})"
        )

        NotificationService.add_notification(event_participant, cls.get_notification_message(event))

    @classmethod
    def _participate_or_error(cls, data: dict) -> EventParticipant:
        event_participant, created = EventParticipant.objects.get_or_create(data)

        if not created:
            raise EventException(
                f"{event_participant.get_participant} is already participating in {event_participant.event}"
            )

        return event_participant

    @classmethod
    def get_notification_message(cls, event: Event) -> str:
        msg = f"Event {event.name} is in {event.get_time_before_start_text()}"
        msg = msg + f"\n\n{event.description}" if event.description else msg
        return msg

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
