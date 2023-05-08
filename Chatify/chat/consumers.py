# from channels.consumer import SyncConsumer
# from channels.generic.websocket import WebsocketConsumer
#
# from channels.exceptions import StopConsumer
# from asgiref.sync import async_to_sync
#
#
# class MyChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, close_code):
#         pass
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#
#         self.send(text_data=json.dumps({"message": message}))