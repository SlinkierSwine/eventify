import logging
from typing import Any
from django.contrib.auth import get_user_model
from django.db.models import Model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

UserModel = get_user_model()
logger = logging.getLogger(__name__)


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = UserModel
        fields = ("username", "password")

    def create(self, validated_data: Any) -> Model:

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user
