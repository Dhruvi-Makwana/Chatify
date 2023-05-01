from .views import register, login, chat
from django.urls import path
from .api import RegistrationApi, UserListAPI


urlpatterns_api = [
    path("api/register/", RegistrationApi.as_view(), name="RegistrationApi"),
    path("api/user/", UserListAPI.as_view(), name="UserListAPI"),
]


urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("chat/", chat, name="chat"),
]

urlpatterns += urlpatterns_api
