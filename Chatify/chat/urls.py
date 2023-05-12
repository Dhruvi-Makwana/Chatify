from .views import register, login, chat
from django.urls import path
from .api import (
    RegistrationApi,
    UserListAPI,
    VisibilityStatusAPI,
    LoginAPIView,
    OnlineUserAPI,
    LogoutView,
)

app_name = "chat"

urlpatterns_api = [
    path("api/register/", RegistrationApi.as_view(), name="RegistrationApi"),
    path("api/user/", UserListAPI.as_view(), name="UserListAPI"),
    path("api/visibility-status/", VisibilityStatusAPI.as_view(), name="online"),
    path("api/login/", LoginAPIView.as_view(), name="login"),
    path("chat/api/userdata/", OnlineUserAPI.as_view(), name="userdata"),
    path("logout/", LogoutView.as_view(), name="logout"),
]


urlpatterns = [
    path("register/", register, name="register"),
    path("login_page/", login, name="loginUI"),
    path("chat/", chat, name="showChat"),
]

urlpatterns += urlpatterns_api
