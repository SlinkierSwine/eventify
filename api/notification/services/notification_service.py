import datetime
from typing import Iterable

from event.models import Event, EventParticipant
from notification.models import Notification
from notification.providers.base import BaseNotificationProvider
from notification.providers.choices import NotificationProviderChoices
from notification.providers.get_provider import get_provider


class NotificationService:
    @classmethod
    def add_notification(cls, receiver: EventParticipant, message: str) -> None:
        providers = cls.get_notification_providers(receiver)
        for provider in providers:
            notification = Notification.objects.create(
                event=receiver.event,
                receiver=receiver,
                message=message,
                provider=provider.get_provider_choices_name(),
            )
            task = provider.apply_async(
                kwargs={"notification_id": notification.id},
                eta=cls.get_task_eta(notification.event),
            )
            notification.celery_task_id = task.id
            notification.save()

    @classmethod
    def get_notification_providers(
        cls, receiver: EventParticipant
    ) -> Iterable[BaseNotificationProvider]:
        if receiver.is_anonymous:
            return [get_provider(receiver.anonymous_participant.notification_provider)]
        else:
            notification_providers = [c[0] for c in NotificationProviderChoices.choices]
            provider_names = receiver.user.social_accounts.filter(
                provider__in=notification_providers, use_for_notifications=True
            ).all()
            return [get_provider(name) for name in provider_names]

    @classmethod
    def get_task_eta(cls, event: Event) -> datetime.datetime:
        return event.start_datetime - datetime.timedelta(
            minutes=event.notify_before_minutes
        )
