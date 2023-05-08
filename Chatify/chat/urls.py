from .views import register, login, chat, websocket
from django.urls import path
from .api import (
    RegistrationApi,
    UserListAPI,
    UserOnlineAPIView,
    LoginAPIView,
    ShowUserData,
)

app_name = "chat"

urlpatterns_api = [
    path("api/register/", RegistrationApi.as_view(), name="RegistrationApi"),
    path("api/user/", UserListAPI.as_view(), name="UserListAPI"),
    path("api/online/", UserOnlineAPIView.as_view(), name="online"),
    path("api/login/", LoginAPIView.as_view(), name="login"),
    path("chat/api/userdata/", ShowUserData.as_view(), name="userdata"),
]


urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login1"),
    path("chat/", chat, name="showChat"),
    path("websocket/", websocket, name="websocket"),

]

urlpatterns += urlpatterns_api
