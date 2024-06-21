import datetime

import factory

from core.utils import get_tomorrow_date
from event.models import Event
from event.tests.utils import get_datetime_for_event


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Faker("word")
    start_datetime = get_datetime_for_event(
        get_tomorrow_date(),
        "10:00",
    )
    end_datetime = get_datetime_for_event(
        get_tomorrow_date(),
        "11:00",
    )

    created_by = factory.SubFactory("account.tests.factories.UserFactory")
