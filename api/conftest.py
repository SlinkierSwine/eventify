import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_with_credentials(request, api_client):
    def authenticate(user):
        api_client.force_authenticate(user=user)
        return api_client

    def logout():
        api_client.force_authenticate(user=None)

    request.addfinalizer(logout)

    return authenticate
