from django.urls import path, re_path
from chat.consumers import VisibilityStatusConsumer

websocket_urlpatterns = [
    path("ws/chat/", VisibilityStatusConsumer.as_asgi()),
]
