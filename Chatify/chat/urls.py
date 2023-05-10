from .views import register, login, chat
from django.urls import path
from .api import (
    RegistrationApi,
    UserListAPI,
    VisibilityStatusAPI,
    LoginAPIView,
    OnlineUserAPI,
)

app_name = "chat"

urlpatterns_api = [
    path("api/register/", RegistrationApi.as_view(), name="RegistrationApi"),
    path("api/user/", UserListAPI.as_view(), name="UserListAPI"),
    path("api/online/", VisibilityStatusAPI.as_view(), name="online"),
    path("api/login/", LoginAPIView.as_view(), name="login"),
    path("chat/api/userdata/", OnlineUserAPI.as_view(), name="userdata"),
]


urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="loginUI"),
    path("chat/", chat, name="showChat"),
]

urlpatterns += urlpatterns_api
