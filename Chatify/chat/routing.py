from django.urls import path, re_path
from chat.consumers import VisibilityStatusConsumer, ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/", VisibilityStatusConsumer.as_asgi()),
    path("ws/chat/message/", ChatConsumer.as_asgi()),
]
