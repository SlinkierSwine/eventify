from django.urls import reverse
import pytest
from rest_framework import status

login_url = "account:login"
registration_url = "account:registration"


@pytest.mark.parametrize(
    "email, password, expected_code",
    [
        ("right@email.com", "RightPassword123", status.HTTP_200_OK),
        ("wrong@email.com", "RightPassword123", status.HTTP_401_UNAUTHORIZED),
        ("right@email.com", "WrongPassword", status.HTTP_401_UNAUTHORIZED),
    ]
)
def test_login_view(email, password, expected_code, api_client, db):
    api_client.post(reverse(registration_url), data={"email": "right@email.com", "password": "RightPassword123"})

    response = api_client.post(reverse(login_url), data={"email": email, "password": password})

    assert response.status_code == expected_code
