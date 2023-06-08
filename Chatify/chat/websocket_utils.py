from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_chat_message(user_id, logout):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "visiblity-group",
        {"type": "chat.message", "id": user_id, "logout": logout},
    )


def get_group_name(current_user, receiver_user):
    if current_user > receiver_user:
        return f"chat_{current_user}_{receiver_user}"
    else:
        return f"chat_{receiver_user}_{current_user}"
