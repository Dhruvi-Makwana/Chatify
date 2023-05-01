from .views import register, login, chat
from django.urls import path
from .api import RegistrationApi, UserListAPI

urlpatterns = [
    path("api/register/", RegistrationApi.as_view(), name="RegistrationApi"),
    path("api/user/", UserListAPI.as_view(), name="UserListAPI"),
]


urlpatterns_templates = [
    path("register/", register, name="user_register"),
    path("login/", login, name="user_register"),
    path("chat/", chat, name="chat"),
]

urlpatterns += urlpatterns_templates
