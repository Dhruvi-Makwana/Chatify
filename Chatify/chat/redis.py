from .models import User
from .websocket_utils import send_chat_message
from django.utils import timezone
import redis


def check_last_login(user_id):

    current_user = User.objects.get(id=user_id)
    utc_now = timezone.now()
    time_diff = utc_now - current_user.last_login
    current_user.last_login = utc_now
    current_user.save()
    print(current_user.last_login)
    if time_diff.total_seconds() > 20:
        # call the function to send chat message
        send_chat_message(user_id, "login")


