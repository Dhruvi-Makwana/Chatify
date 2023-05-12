from channels.consumer import SyncConsumer


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({"type": "websocket.accept"})

    def websocket_receive(self, event):
        pass

    def websocket_disconnect(self, event):
        pass
