from django.urls import path
from chat.consumers import MySyncConsumer

websocket_urlpatterns = [
    path("ws/sc/", MySyncConsumer.as_asgi()),
    # path('chat/sc', MyChatConsumer.as_asgi()),
]
