import datetime
from typing import Any

from django.contrib.auth import get_user_model
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

    created_by = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="created_events"
    )

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return f"Event '{self.name}'"

    def clean(self) -> None:
        if self.start_datetime <= datetime.datetime.now(datetime.UTC):
            raise ValidationError({"start_time": "You can't create events in the past"})
        if self.start_datetime >= self.end_datetime:
            raise ValidationError(
                {"start_time": "Start datetime should be before end datetime"}
            )
        return super().clean()

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)


class AnonymousParticipant(TimeStampableModel):
    social_contact = models.CharField(
        "social contact", max_length=256, help_text="Id of social account"
    )
    notification_provider = models.CharField(
        "notification provider", choices=NotificationProvider.choices, max_length=128
    )

    class Meta:
        verbose_name = "AnonymousParticipant"
        verbose_name_plural = "AnonymousParticipants"

    def __str__(self):
        return f"AnonymousParticipant {self.pk}"


class EventParticipant(models.Model):
    event = models.ForeignKey(
        "Event", on_delete=models.CASCADE, related_name="participants"
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="participating_events",
        blank=True,
        null=True,
    )
    anonymous_participant = models.ForeignKey(
        "AnonymousParticipant",
        on_delete=models.CASCADE,
        related_name="participating_events",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"EventParticipant {self.pk}"

    def clean(self) -> None:
        if self.user and self.anonymous_participant:
            raise ValidationError(
                {
                    "anonymous_participant": "Event participant can be only user or anonymous, but not at the same time"
                }
            )
        if not (self.user and self.anonymous_participant):
            raise ValidationError(
                {
                    "anonymous_participant": "Event participant should have at least one of user or anonymous"
                }
            )
        return super().clean()
