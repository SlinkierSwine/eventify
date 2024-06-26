from notification.exceptions import NotificationProviderException
from notification.providers.base_provider import BaseNotificationProvider
from notification.providers.choices import NotificationProviderChoices
from notification.providers.email_provider import EmailNotificationProvider

_PROVIDERS_MAPPING = {
    NotificationProviderChoices.EMAIL: EmailNotificationProvider,
}


def get_provider(name: NotificationProviderChoices) -> BaseNotificationProvider:
    provider = _PROVIDERS_MAPPING.get(name)

    if not provider:
        raise NotificationProviderException("No such notification provider: ", name)

    return provider
