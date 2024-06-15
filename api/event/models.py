from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.exceptions import ValidationError
from django.db import models

from core.models import TimeStampableModel
from notification.models import NotificationProvider

UserModel = get_user_model()


class Event(TimeStampableModel):
    name = models.CharField("name", max_length=256)
    description = models.TextField("description", blank=True, null=True)

    start_datetime = models.DateTimeField("start datetime")
    end_datetime = models.DateTimeField("end datetime")

    is_canceled = models.BooleanField("is canceled", default=False)
    is_private = models.BooleanField("is private", default=False)

    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="created_events")

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def clean(self) -> None:
        if self.start_datetime > self.end_datetime:
            raise ValidationError(
                {"start_time": "Start datetime should be before end datetime"}
            )
        return super().clean()

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)


class AnonymousParticipant(TimeStampableModel):
    social_contact = models.CharField("social contact", max_length=256, help_text="Id of social account")
    notification_provider = models.CharField("notification provider", choices=NotificationProvider.choices, max_length=128)

    participating_event = GenericRelation("EventParticipant", related_query_name="anonymous_participants")

    class Meta:
        verbose_name = "AnonymousParticipant"
        verbose_name_plural = "AnonymousParticipants"


class EventParticipant(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE)

    participant_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    participant_id = models.PositiveIntegerField()
    participant = GenericForeignKey("participant_content_type", "participant_id")

