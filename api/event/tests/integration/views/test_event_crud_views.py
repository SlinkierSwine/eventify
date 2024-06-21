import pytest
from django.urls import reverse
from rest_framework import status

from core.utils import get_tomorrow_date, get_yesterday_date
from event.tests.utils import get_datetime_for_event

event_create_url = "event:event_create"
event_retrieve_update_destroy_url = "event:event_retrieve_update_destroy"


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
    response = api_client.post(reverse(event_create_url), data=data)

    assert response.status_code == expected_code


@pytest.mark.parametrize(
    "data, expected_code",
    [
        ({"name": "New name"}, status.HTTP_200_OK),
        ({"description": "New description"}, status.HTTP_200_OK),
        (
            {"start_datetime": get_datetime_for_event(get_tomorrow_date(), "5:00")},
            status.HTTP_200_OK,
        ),
        (
            {
                "start_datetime": get_datetime_for_event(get_tomorrow_date(), "15:00"),
                "end_datetime": get_datetime_for_event(get_tomorrow_date(), "16:00"),
            },
            status.HTTP_200_OK,
        ),
    ],
)
def test_update_event_view(data, expected_code, event, api_client_with_credentials, db):
    user = event.created_by
    api_client = api_client_with_credentials(user)

    url = reverse(event_retrieve_update_destroy_url, kwargs={"pk": event.pk})
    response = api_client.patch(url, data=data)

    assert response.status_code == expected_code

    event.refresh_from_db()
    for key, value in data.items():
        assert getattr(event, key) == value
