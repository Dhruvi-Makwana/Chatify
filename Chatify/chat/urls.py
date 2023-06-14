from .views import register, login, chat
from django.urls import path
from .api import (
    RegistrationApi,
    UserListAPI,
    VisibilityStatusAPI,
    LoginAPIView,
    OnlineUsersAPI,
    LogoutView,
    SetUserActiveTime,
    CheckUserActivity,
    ChatMessages,
    BlockUserAPI,
    PdfDownloadAPI,
    HomePage,
)

app_name = "chat"

urlpatterns_api = [
    path("api/register/", RegistrationApi.as_view(), name="RegistrationApi"),
    path("api/user/", UserListAPI.as_view(), name="UserListAPI"),
    path(
        "api/visibility-status/",
        VisibilityStatusAPI.as_view(),
        name="VisibilityStatusAPI",
    ),
    path("api/login/", LoginAPIView.as_view(), name="login"),
    path("chat/api/get_online_user/", OnlineUsersAPI.as_view(), name="get_online_user"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "chat/api/set-user-active-time/",
        SetUserActiveTime.as_view(),
        name="SetUserActiveTime",
    ),
    path(
        "chat/api/get-user-from-redis/",
        CheckUserActivity.as_view(),
        name="CheckUserActive",
    ),
    path("chat/api/messages/<int:pk>", ChatMessages.as_view(), name="chat_message"),
    path("chat/api/block-user/", BlockUserAPI.as_view(), name="block_user"),
    path("chat/pdf_download/<int:pk>", PdfDownloadAPI.as_view(), name="pdf_download"),
    path("homepage/<int:pk>", HomePage.as_view()),
]


urlpatterns = [
    path("register/", register, name="register"),
    path("login_page/", login, name="loginUI"),
    path("chat/", chat, name="showChat"),
]

urlpatterns += urlpatterns_api
