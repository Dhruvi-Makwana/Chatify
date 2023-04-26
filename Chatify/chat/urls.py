from django.urls import path
from .views import *


urlpatterns = [
    path("chatui/",chat,name="chatui"),
]