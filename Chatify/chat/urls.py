from .views import RegisterView
from django.urls import include, path

app_name = 'chat'
urlpatterns = [
    path('user_register/', RegisterView.as_view(), name='user_register'),
]