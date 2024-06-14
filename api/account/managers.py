from account.exceptions import CreateSuperUserException, CreateUserException
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str):
        if email is None:
            raise CreateUserException("Users must have an email address.")
        if password is None:
            raise CreateUserException("Users must have a password.")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def make_superuser(self, user) -> None:
        user.is_superuser = True
        user.is_staff = True

    def create_superuser(self, email: str, password: str):
        if password is None:
            raise CreateSuperUserException("Superusers must have a password.")

        user = self.create_user(email, password)
        self.make_superuser(user)
        user.save()

        return user

    def one_or_none(self, email: str):
        try:
            user = self.get_queryset().get(email=email.lower())
        except self.model.DoesNotExist:
            return None
        return user
