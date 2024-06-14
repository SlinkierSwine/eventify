from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from account.managers import UserManager
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
