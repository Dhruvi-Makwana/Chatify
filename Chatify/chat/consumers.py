from channels.consumer import SyncConsumer
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
                    {"user_id": self.scope["user"].id, "status": status}
                ),
            }
        )

    def websocket_disconnect(self, event):
        pass
