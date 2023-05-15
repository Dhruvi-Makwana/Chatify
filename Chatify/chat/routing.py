from django.urls import path, re_path
from chat.consumers import ChatConsumer, MyConsumer

websocket_urlpatterns = [
    path("ws/chat/", ChatConsumer.as_asgi()),
    path("ws/chat/<str:room_name>/", MyConsumer.as_asgi()),

]
