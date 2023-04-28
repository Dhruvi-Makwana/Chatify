from .views import register, login, chat
from django.urls import include, path

app_name = "chat"
urlpatterns = [
    path("register/", register, name="user_register"),
    path("login/", login, name="user_register"),
    path("chat/", chat, name="chat"),
]
