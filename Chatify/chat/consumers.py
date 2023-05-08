from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync


class MyChatConsumer(SyncConsumer):

    def websocket_connect(self, event):
        # async_to_sync(self.channel_layer.group_add)('programmers' ,self.channel_name)
        print("connection Accept")
        self.send({
            "type" :'websocket.accept'
        })

    def websocket_receive(self, event):
        print("message Recevied" ,event)
        # async_to_sync(self.channel_layer.group_send)(
        #     'programmers' ,{
        #         'type' :'chat.message',
        #         'message' :event['text']
        #     })

    # def chat_message(self ,event):
    #     print("message in handler" ,event)
    #     self.send({
    #         'type': 'websocket.send',
    #         'text': event['message']
    #     })

    def websocket_disconnect(self, event):
        pass