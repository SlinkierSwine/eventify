from event.models import EventParticipant
from notification.exceptions import NotificationProviderException
from notification.providers.choices import NotificationProviderChoices


class EventParticipantService:
    @classmethod
    def get_social_contact(
        cls,
        event_participant: EventParticipant,
        notification_provider: NotificationProviderChoices,
    ) -> str:
        participant = event_participant.get_participant()
        if event_participant.is_anonymous:
            if participant.notification_provider != notification_provider:
                raise NotificationProviderException(f"{participant} does not have {notification_provider} social account")

            return participant.social_contact

        if notification_provider == NotificationProviderChoices.EMAIL:
            return participant.email

        social_account = participant.social_accounts.get(provider=notification_provider)
        return social_account.social_contact
