import datetime

import factory

from event.models import Event
from core.utils import get_tomorrow_date


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Faker("word")
    start_datetime = datetime.datetime.combine(
        date=get_tomorrow_date(), time=datetime.time(hour=10)
    )
    end_datetime = datetime.datetime.combine(
        date=get_tomorrow_date(), time=datetime.time(hour=11)
    )

    created_by = factory.SubFactory("UserFactory")
