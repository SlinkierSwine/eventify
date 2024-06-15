from django.db import models


class NotificationProvider(models.TextChoices):
    TELEGRAM = "telegram"
    VK = "vk"
    EMAIL = "email"
    WEB = "web"
