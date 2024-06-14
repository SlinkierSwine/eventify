from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


def validate_unique_user(email: str) -> None:
    user = UserModel.objects.filter(email=email.lower())
    if user.exists():
        raise serializers.ValidationError(
            "This email is already associated with an account."
        )
