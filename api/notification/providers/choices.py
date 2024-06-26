from django.db import models

from account.social_account_choices import SocialAccountChoices


class NotificationProviderChoices(models.TextChoices):
    EMAIL = SocialAccountChoices.EMAIL
    WEB = "web"
    VK = SocialAccountChoices.VK
    GOOGLE = SocialAccountChoices.GOOGLE
    TELEGRAM = SocialAccountChoices.TELEGRAM
