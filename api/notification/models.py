from django.db import models

from core.models import TimeStampableModel
from notification.providers.choices import NotificationProviderChoices


class Notification(TimeStampableModel):
    message = models.TextField("message")
    provider = models.CharField(
        "provider", choices=NotificationProviderChoices.choices, max_length=128
    )
    celery_task_id = models.IntegerField("celery task id", null=True, blank=True)

    receiver = models.ForeignKey(
        "event.EventParticipant",
        on_delete=models.CASCADE,
        related_name="received_notifications",
    )
    event = models.ForeignKey(
        "event.Event",
        on_delete=models.CASCADE,
        related_name="notifications",
    )

