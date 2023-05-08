from django.urls import path
# from chat.consumers import MySyncConsumer,MyChatConsumer
from chat.consumers import MyChatConsumer

websocket_urlpatterns = [
    path('chat/sc/', MyChatConsumer.as_asgi()),
]
