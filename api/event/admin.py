from django.contrib import admin

from event.models import AnonymousParticipant, Event, EventParticipant


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(AnonymousParticipant)
class AnonymousParticipantAdmin(admin.ModelAdmin):
    pass


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    pass
