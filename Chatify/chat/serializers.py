from .models import User
from rest_framework import serializers
from .utils import *


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        max_length=255, write_only=True, required=False
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "profile_photo",
            "mobile_number",
            "password",
            "confirm_password",
            "is_online",
        )

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        instance = super().create(validated_data)
        raw_password = validated_data.get("password")
        if raw_password:
            instance.set_password(raw_password)
        instance.save()
        return instance

    def validate_password(self, password):
        confirmation_password = self.initial_data.get("confirm_password")
        if password and confirmation_password:
            if password != confirmation_password:
                raise serializers.ValidationError("PASSWORD DOESNOT MATCH")
        return password

    def validate_mobile_number(self, mobile_number):
        breakpoint()
        return mobile_number
