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
                raise serializers.ValidationError("Password doesn't match")
        return password


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.CharField()
    profile = serializers.URLField()
    message = serializers.CharField()


class GetUserDataSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    messages = MessageSerializer(read_only=True)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = User
        fields = (
            "username",
            "profile_photo",
            "is_online",
            "full_name",
            "messages",
        )
