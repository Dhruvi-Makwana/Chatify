from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("connection Accept")
        self.send({"type": "websocket.accept"})

    def websocket_receive(self, event):
        pass

    def websocket_disconnect(self, event):
        pass
