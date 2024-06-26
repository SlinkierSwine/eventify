from django.db import models


class SocialAccountChoices(models.TextChoices):
    VK = "vk"
    GOOGLE = "google"
    TELEGRAM = "telegram"
    EMAIL = "email"
