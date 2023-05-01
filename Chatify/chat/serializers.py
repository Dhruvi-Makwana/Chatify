from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=255, write_only=True)

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
        )

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        instance = super().create(validated_data)
        raw_password = validated_data.get("password")
        instance.set_password(raw_password)
        instance.save()
        return instance

    def validate_password(self, attrs):
        confirmation_password = self.initial_data.get("confirm_password")
        if not attrs == confirmation_password:
            raise serializers.ValidationError("PASSWORD DOESNOT MATCH")
        return attrs
