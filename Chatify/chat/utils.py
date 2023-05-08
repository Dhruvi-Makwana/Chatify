from rest_framework import serializers
from rest_framework import status


def set_contact_number(data):
    get_mobile_number = data.get("mobile_number")
    if len(get_mobile_number) > 10 and len(get_mobile_number) <= 13:
        if get_mobile_number[:2] == "91":
            data["mobile_number"] = "+" + get_mobile_number
        elif get_mobile_number[:3] != "+91":
            raise serializers.ValidationError(
                {"phone_number": "Phone number is Not Valid"}
            )
    elif len(get_mobile_number) == 10:
        data["mobile_number"] = "+91" + get_mobile_number
    return data
