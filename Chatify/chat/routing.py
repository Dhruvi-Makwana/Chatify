from django.urls import path, re_path
from chat.consumers import MyConsumer

websocket_urlpatterns = [
    path("ws/chat/", MyConsumer.as_asgi()),
]
