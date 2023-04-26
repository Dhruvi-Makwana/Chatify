from .views import register, login
from django.urls import include, path

app_name = "chat"
urlpatterns = [
    path("user_register/", register, name="user_register"),
    path("login/", login, name="user_register"),
]
