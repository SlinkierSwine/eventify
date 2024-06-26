from django.urls import reverse
import pytest
from rest_framework import status

registration_url = "account:registration"


@pytest.mark.parametrize(
    "email, password, expected_code",
    [
        ("right@email.com", "RightPassword123", status.HTTP_201_CREATED),
        ("wrongemail.com", "RightPassword123", status.HTTP_400_BAD_REQUEST),
        ("right@email.com", "", status.HTTP_400_BAD_REQUEST),
        ("", "", status.HTTP_400_BAD_REQUEST),
    ]
)
def test_registration_view(email, password, expected_code, api_client, db):
    response = api_client.post(reverse(registration_url), data={"email": email, "password": password})

    assert response.status_code == expected_code


def test_cant_register_twice(api_client, db):
    data = {"email": "test@email.com", "password": "TestPassword123"}
    api_client.post(reverse(registration_url), data=data)

    response = api_client.post(reverse(registration_url), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
