from .websocket_utils import send_chat_message
import redis
from django.utils import timezone
import pytz


def check_last_login(user_id):
    r = redis.Redis()
    last_login = r.get(f"user:{user_id}:last_login")
    last_update_time = timezone.datetime.fromtimestamp(float(last_login), pytz.utc)
    current_dt = timezone.now().astimezone(pytz.utc)
    send_chat_message(user_id, "login")
    r.set(f"user:{user_id}:last_login", timezone.now().timestamp())
