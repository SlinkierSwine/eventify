import logging

from core.services.send_email import send_email
from event.services.event_participant_service import EventParticipantService
from eventify.celery import app
from notification.models import Notification
from notification.providers.base_provider import BaseNotificationProvider
from notification.providers.choices import NotificationProviderChoices

logger = logging.getLogger(__name__)


class EmailNotificationProvider(BaseNotificationProvider):
    def notify(self, notification: Notification) -> None:
        email = EventParticipantService.get_social_contact(
            notification.receiver, notification.provider
        )
        subject = f"'{notification.event.name}' is coming soon!"
        send_email(email, subject, notification.message)

    @classmethod
    def get_provider_choices_name(cls) -> NotificationProviderChoices:
        return NotificationProviderChoices.EMAIL


EmailNotificationProvider = app.register_task(EmailNotificationProvider())
