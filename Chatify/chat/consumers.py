from channels.generic.websocket import (
    AsyncWebsocketConsumer,
    AsyncJsonWebsocketConsumer,
)
from asgiref.sync import sync_to_async
import json
from .models import Chat


class VisibilityStatusConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("visiblity-group", self.channel_name)
        await self.accept()

    async def receive_json(self, event):
        await self.channel_layer.group_send(
            "visiblity-group",
            {
                "type": "chat.message",
            },
        )

    @sync_to_async
    def updated_instance(self):
        from .models import User

        instance = User.objects.get(id=self.scope["user"].id)
        return instance

    async def chat_message(self, event):
        from .serializers import UserSerializer

        modify_instance = await self.updated_instance()
        serializer = UserSerializer(instance=modify_instance)
        await self.send_json(serializer.data),

    async def disconnect(self, event):
        await self.channel_layer.group_discard("visiblity-group", self.channel_name)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.current_user_id = self.scope["user"].id
        self.other_user_id = self.scope["url_route"]["kwargs"]["id"]
        self.group_name = (
            f"chat_{self.current_user_id}_{self.other_user_id}"
            if self.current_user_id > self.other_user_id
            else f"chat_{self.other_user_id}_{self.current_user_id}"
        )
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["msg"]
        receiver = text_data_json["receiverId"]
        sender = self.scope["user"].id
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": message,
                "sender": sender,
                "receiver": receiver,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        response = [
            {
                "user": self.scope["user"].username,
                "profile": self.scope["user"].profile_photo.url,
                "message": message,
                "sendId": self.scope["user"].id,
            }
        ]

        await self.send(text_data=json.dumps(response))
