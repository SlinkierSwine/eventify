from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from account.managers import UserManager
from account.social_account_choices import SocialAccountChoices
from core.models import TimeStampableModel


class User(AbstractBaseUser, TimeStampableModel, PermissionsMixin):
    email = models.EmailField("email", unique=True)
    name = models.CharField("name", max_length=128, blank=True, null=True)

    is_staff = models.BooleanField("staff status", default=False)
    is_active = models.BooleanField("active", default=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self) -> str:
        return f"User {self.pk}: {self.email}"


class SocialAccount(TimeStampableModel):
    provider = models.CharField("provider", choices=SocialAccountChoices.choices)
    use_for_notifications = models.BooleanField("use for notifications", default=True)

    social_contact = models.CharField("social contact", max_length=256, blank=True, null=True)

    access_token = models.CharField("access token", max_length=256, blank=True, null=True)
    refresh_token = models.CharField("refresh token", max_length=256, blank=True, null=True)
    extra_data = models.JSONField("extra data", blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_accounts")

    class Meta:
        verbose_name = "SocialAccount"
        verbose_name_plural = "SocialAccounts"
    
    def __str__(self):
        return f"SocialAccount {self.pk}, {self.provider}"
