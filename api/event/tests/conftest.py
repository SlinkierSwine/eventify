import pytest

from account.tests.factories import UserFactory


@pytest.fixture
def user(db):
    return UserFactory()
