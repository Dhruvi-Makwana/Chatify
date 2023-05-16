from channels.consumer import SyncConsumer, AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json


class ChatConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({"type": "websocket.accept"})

    def websocket_receive(self, event):
        status = json.loads(event.get("text")).get("status")
        self.send(
            {
                "type": "websocket.send",
                "text": json.dumps(
                    {
                        "id": self.scope["user"].id,
                        "full_name": self.scope["user"].get_full_name(),
                        "profile_photo": self.scope["user"].profile_photo.url,
                        "status": status,
                    }
                ),
            }
        )

    def websocket_disconnect(self, event):
        pass


class MyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("visiblity-group", self.channel_name)
        await self.accept()

    async def receive_json(self, event):
        status = event.get("status")
        json_data = {
            "message": event,
            "user_id": self.scope["user"].id,
            "full_name": self.scope["user"].get_full_name(),
            "profile_photo": self.scope["user"].profile_photo.url,
            "status": status,
        }
        # Send message to group
        await self.channel_layer.group_send(
            "visiblity-group",
            {
                "type": "chat.message",
                "text": json.dumps(json_data),
            },
        )

    async def chat_message(self, event):
        status = json.loads(event.get("text")).get("status")
        await self.send_json(
            {
                "user_id": self.scope["user"].id,
                "full_name": self.scope["user"].get_full_name(),
                "profile_photo": self.scope["user"].profile_photo.url,
                "status": status,
            }
        ),

    async def disconnect(self, event):
        await self.channel_layer.group_discard("visiblity-group", self.channel_name)
