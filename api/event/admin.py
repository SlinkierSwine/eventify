from django.contrib import admin

from event.models import AnonymousParticipant, Event, EventParticipant


@admin.register(AnonymousParticipant)
class AnonymousParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "social_contact", "notification_provider")


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "anonymous_participant")


class EventParticipantInline(admin.TabularInline):
    model = EventParticipant


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "start_datetime",
        "end_datetime",
        "created_by",
        "is_canceled",
        "is_private",
    )
    list_filter = ("is_canceled", "is_private", "start_datetime")

    inlines = (EventParticipantInline,)
