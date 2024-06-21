import pytest

from account.tests.factories import UserFactory
from event.tests.factories import EventFactory


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def event(user):
    return EventFactory(created_by=user)
