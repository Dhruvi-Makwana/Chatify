from channels.generic.websocket import (
    AsyncWebsocketConsumer,
    AsyncJsonWebsocketConsumer,
)
from asgiref.sync import sync_to_async
import json


class VisibilityStatusConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("visiblity-group", self.channel_name)
        await self.accept()

    async def receive_json(self, event):
        user_id = event.get("Userid")
        logout = event.get("logout")
        await self.channel_layer.group_send(
            "visiblity-group",
            {"type": "chat.message", "id": user_id, "logout": logout},
        )

    @sync_to_async
    def updated_instance(self, user_id):
        from .models import User

        instance = User.objects.get(id=user_id)
        return instance

    async def chat_message(self, event):
        from .serializers import UserSerializer

        userid = event.get("id")
        logout = event.get("logout")
        modify_instance = await self.updated_instance(userid)
        serializer = UserSerializer(instance=modify_instance)
        await self.send_json({"data": serializer.data, "user_auth": logout})

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

    @sync_to_async
    def send_data_to_save_chat(self, sender, msg, get_date, timezone):
        from .models import ChatGroup, Chat, User
        from datetime import datetime

        sender_id = User.objects.get(id=int(sender))
        instance, created = ChatGroup.objects.get_or_create(name=self.group_name)

        Chat.objects.create(
            message=msg,
            sent_at=datetime.strptime(get_date, "%d/%m/%Y, %I:%M:%S %p"),
            client_timezone=timezone,
            group=instance,
            sender=sender_id,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender_id = text_data_json["senderId"]
        message = text_data_json["msg"]
        client_time = text_data_json["date"]
        tz = text_data_json['timezone']
        await self.send_data_to_save_chat(sender_id, message, client_time, tz)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": message,
                "sender_id": sender_id,
                "date": client_time,
            },
        )

    @sync_to_async
    def get_instance(self, sender_id):
        from .models import User

        instance = User.objects.get(id=sender_id)
        return instance

    async def chat_message(self, event):
        from .serializers import UserSerializer

        update_instance = await self.get_instance(int(event["sender_id"]))
        serializer_data = UserSerializer(instance=update_instance).data
        serializer_data["message"] = event["message"]
        serializer_data["sender"] = int(event["sender_id"])
        serializer_data["sent_at"] = event["date"]
        await self.send(json.dumps(serializer_data))

    async def disconnect(self, event):
        await self.channel_layer.group_discard("visiblity-group", self.channel_name)
