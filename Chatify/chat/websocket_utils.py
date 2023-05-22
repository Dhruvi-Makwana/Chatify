from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_chat_message(user_id, logout):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "visiblity-group",
        {"type": "chat.message", "id": user_id, "logout": logout},
    )
