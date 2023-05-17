from channels.consumer import SyncConsumer, AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json


class MyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("visiblity-group", self.channel_name)
        await self.accept()

    async def receive_json(self, event):
        status = event.get("status")
        json_data = {
            "message": event,
            "id": self.scope["user"].id,
            "full_name": self.scope["user"].get_full_name(),
            "profile_photo": self.scope["user"].profile_photo.url,
            "status": status,
        }
        await self.channel_layer.group_send(
            "visiblity-group",
            {
                "type": "chat.message",
                "text": json.dumps(json_data),
            },
        )

    async def chat_message(self, event):
        from .serializers import GetUserDataSerializer

        serializer = GetUserDataSerializer(instance=self.scope["user"])
        await self.send_json(serializer.data),

    async def disconnect(self, event):
        await self.channel_layer.group_discard("visiblity-group", self.channel_name)
