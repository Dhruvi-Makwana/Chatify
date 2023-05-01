from .views import register, login, chat
from django.urls import include, path

app_name = "chat"
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("chat/", chat, name="chat"),
]
