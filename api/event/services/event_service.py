from typing import Iterable

from django.contrib.auth.base_user import AbstractBaseUser

from event.exceptions import EventException
from event.models import AnonymousParticipant, Event, EventParticipant


class EventService:
    @classmethod
    def create_event_participants(
        cls,
        event: Event,
        participants: Iterable[AbstractBaseUser | AnonymousParticipant],
    ):
        for participant in participants:

            if isinstance(participant, AbstractBaseUser):
                event_participant, created = EventParticipant.objects.get_or_create(
                    event=event, user=participant
                )
                if not created:
                    raise EventException(
                        f"{participant} is already participating in {event}"
                    )

            elif isinstance(participant, AnonymousParticipant):
                event_participant, created = EventParticipant.objects.get_or_create(
                    event=event, anonymous_participant=participant
                )
                if not created:
                    raise EventException(
                        f"Participant with {participant.notification_provider} ID = {participant.social_contact} is already participating in {event}"
                    )

            else:
                raise EventException(
                    "Event participant can be only user or anonymous participant"
                )

            event.participants.add(event_participant)
