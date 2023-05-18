from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async


class VisibilityStatusConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("visiblity-group", self.channel_name)
        await self.accept()

    async def receive_json(self, event):

        user_id = event.get("Userid")
        await self.channel_layer.group_send(
            "visiblity-group",
            {
                "type": "chat.message",
                "id": user_id,
            },
        )

    @sync_to_async
    def updated_instance(self, user_id):
        from .models import User

        instance = User.objects.get(id=user_id)
        return instance

    async def chat_message(self, event):
        from .serializers import UserSerializer

        userid = event.get("id")
        modify_instance = await self.updated_instance(userid)
        serializer = UserSerializer(instance=modify_instance)
        await self.send_json(serializer.data),

    async def disconnect(self, event):
        await self.channel_layer.group_discard("visiblity-group", self.channel_name)
