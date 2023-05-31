from .models import User, Chat, ChatGroup
from rest_framework import serializers
from .utils import *
from .constants import PASSWORD_ERROR_MESSAGE


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        max_length=255, write_only=True, required=False
    )
    full_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_profile_photo(self, obj):
        return obj.profile_photo.url

    def get_status(self, obj):
        return "online" if obj.is_online else "offline"

    def get_messages(self, obj):
        messages = Chat.objects.all()
        message_serializer = ChatSerializer(messages, many=True)
        return message_serializer.data

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "profile_photo",
            "mobile_number",
            "password",
            "confirm_password",
            "is_online",
            "last_login",
            "status",
            "full_name",
            "messages",
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
                raise serializers.ValidationError(PASSWORD_ERROR_MESSAGE)
        return password


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"
