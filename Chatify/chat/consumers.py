from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
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
