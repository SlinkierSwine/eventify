import abc
import logging
from typing import Any

import celery

from notification.models import Notification
from notification.providers.choices import NotificationProviderChoices

logger = logging.getLogger(__name__)


class BaseNotificationProvider(abc.ABC, celery.Task):
    def run(self, *args: Any, **kwargs: Any) -> None:
        notification_id = kwargs.get("notification_id")
        notification = Notification.objects.filter(pk=notification_id).first()

        if not notification:
            logger.error(f"{self.__class__.__name__}: no notification with {notification_id} id")
            raise Notification.DoesNotExist
    
        self.notify(notification)

    @abc.abstractmethod
    def notify(self, notification: Notification) -> None:
        ...

    @classmethod
    @abc.abstractmethod
    def get_provider_choices_name(cls) -> NotificationProviderChoices:
        ...
