from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async


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
