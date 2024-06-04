from django.contrib.auth.models import AbstractUser

from core.models import TimeStampableModel


class User(AbstractUser, TimeStampableModel):
    # Remove default date_joined field, as we already have it in TimeStampableModel
    date_joined = None
