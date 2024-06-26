import logging
from typing import Any
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.social_account_choices import SocialAccountChoices
from account.validators import validate_unique_user
from account.models import SocialAccount

UserModel = get_user_model()
logger = logging.getLogger(__name__)


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            validate_email,
            validate_unique_user,
        ],
    )
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = UserModel
        fields = ("email", "password")

    def create(self, validated_data: Any) -> Model:
        email = validated_data["email"].lower()

        logger.info(f"Creating new user, email = {email}")

        with transaction.atomic():
            user = UserModel.objects.create_user(
                email=email,
                password=validated_data['password'],
            )
            SocialAccount.objects.create(provider=SocialAccountChoices.EMAIL, user=user)

            return user


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Any) -> Any:
        attrs["email"] = attrs["email"].lower()
        data = super().validate(attrs)

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", "email", "name")
        read_only_fields = ("email",)
