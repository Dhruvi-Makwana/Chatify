from .views import register, login, chat
from django.urls import path

# app_name = "chat"

urlpatterns = [
    path("user_register/", register, name="user_register"),
    path("login/", login, name="login"),
    path("chatui/", chat, name="chatui"),
]
