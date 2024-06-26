from notification.providers.base import BaseNotificationProvider
from notification.providers.choices import NotificationProviderChoices
from notification.providers.exceptions import ProviderException

_PROVIDERS_MAPPING = {}


def get_provider(name: NotificationProviderChoices) -> BaseNotificationProvider:
    provider = _PROVIDERS_MAPPING.get(name)

    if not provider:
        raise ProviderException("No such notification provider: ", name)

    return provider
