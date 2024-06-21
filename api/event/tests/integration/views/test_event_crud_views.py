import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from core.utils import get_tomorrow_date, get_yesterday_date

create_event_url = reverse("event:event_create")


def get_datetime_for_event(
    date: datetime.date, time: str, format: str = "%H:%M"
) -> datetime.datetime:
    return datetime.datetime.combine(
        date, datetime.datetime.strptime(time, format).time()
    )


@pytest.mark.parametrize(
    "start_datetime, end_datetime, expected_code",
    [
        (
            get_datetime_for_event(get_tomorrow_date(), "10:00"),
            get_datetime_for_event(get_tomorrow_date(), "11:00"),
            status.HTTP_201_CREATED,
        ),
        (
            get_datetime_for_event(get_tomorrow_date(), "11:00"),
            get_datetime_for_event(get_tomorrow_date(), "10:00"),
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            get_datetime_for_event(get_tomorrow_date(), "10:00"),
            get_datetime_for_event(get_tomorrow_date(), "10:00"),
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            get_datetime_for_event(get_yesterday_date(), "10:00"),
            get_datetime_for_event(get_yesterday_date(), "11:00"),
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
def test_create_event_view(
    start_datetime, end_datetime, expected_code, user, api_client_with_credentials, db
):
    data = {
        "name": "Test Event",
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "created_by": user.id,
    }

    api_client = api_client_with_credentials(user)
    response = api_client.post(create_event_url, data=data)

    assert response.status_code == expected_code
