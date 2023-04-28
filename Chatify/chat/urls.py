from .views import register, login, chat
from django.urls import path
from .api import RegistrationApi

urlpatterns = [
    path("api/register/", RegistrationApi.as_view(), name="RegistrationApi"),
]


urlpatterns_templates = [
    path("register/", register, name="user_register"),
    path("login/", login, name="user_register"),
    path("chat/", chat, name="chat"),
]

urlpatterns += urlpatterns_templates
