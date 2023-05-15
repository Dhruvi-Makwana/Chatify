from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
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


class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "my_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        status = json.loads(text_data).get("status")
        # Send message to group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "send_status",
                "user_id": self.scope["user"].id,
                "full_name": self.scope["user"].get_full_name(),
                "profile_photo": self.scope["user"].profile_photo.url,
                "status": status,
            }
        )

    def send_status(self, event):
        self.send(
            {
                "type": "websocket.send",
                "text": json.dumps(
                    {
                        "id": event["user_id"],
                        "full_name": event["full_name"],
                        "profile_photo": event["profile_photo"],
                        "status": event["status"],
                    }
                ),
            }
        )
